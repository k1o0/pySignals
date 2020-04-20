from __future__ import annotations
import signals as sig
from signals import transfer
from typing import Callable, Tuple, Union, Any, Optional

# Annotations
transferer = Callable[[Tuple['Node'], 'Node', Optional[Callable]], None]


class Node:
    verbose = 0

    def __init__(self, net: sig.Net, srcs: Optional[Tuple, Node] = None, trans_fun: transferer = transfer.identity,
                 trans_arg: Optional[Callable] = None, append_values: bool = False, format_spec: str = None) -> None:
        if srcs is None:
            srcs = tuple()
        assert net.is_valid()
        self.net = net
        self.id = net.next_free_node()
        self.__current_value = list() if append_values else None
        self.__working_value = None
        self._queued = False
        self.queued = False  # Transaction status @todo doesn't need initializing
        self.targets = list()  # List of downstream nodes
        self.inputs = (srcs,) if isinstance(srcs, sig.node.Node) else tuple(srcs)  # Ensure tuple
        self.display_inputs = self.inputs
        self._append_values = append_values
        self.active = True  # Flag for whether in use
        self.transferer = trans_fun
        self.trans_arg = trans_arg
        self.format_spec = format_spec
        net.register_node(self)  # Add node to network node set
        for src in self.inputs:  # Register node with targets
            src.targets.append(self)

    def is_valid(self) -> bool:
        return self.active & (self.id <= self.net.size)

    def name(self) -> str:
        """Name set with format spec"""
        child_names = [n.name() for n in self.display_inputs]
        if self.format_spec is not None:
            name = self.format_spec.format(*child_names)
        else:  # e.g. 'Node #4 <- mapn(t, 2, add)'
            arg_name = self.trans_arg.__name__ if hasattr(self.trans_arg, '__name__') else self.trans_arg
            name = '{} <- {}({}, {})'.format(self, self.transferer.__name__, ', '.join(child_names), arg_name)
        return name

    def __str__(self) -> str:
        return 'Node #{}'.format(self.id)

    @property
    def value(self) -> Any:
        return self.__working_value if self.__working_value is not None else self.__current_value

    @value.setter
    def value(self, v: Any) -> None:
        if v is None:
            return
        self.__working_value = v
        self.queued = True
        for observer in self.targets:  # Notify downstream targets of change
            observer.notify(self, 'updated')

    @property
    def queued(self) -> bool:
        """Get queued status"""
        return self._queued

    @queued.setter
    def queued(self, tf: bool) -> None:
        if tf:
            self._queued = True
        if self._queued and not tf:  # No longer queued
            self.__set__current_value()  # Copy working value to current
            self._queued = False
            for observer in self.inputs:  # Notify upstream targets completed
                observer.notify(self, 'completed')  # @todo record if affected

    def notify(self, observable: Node, event: str) -> None:
        if self.verbose:
            print('{} notified of "{}" event by {}'.format(self, event, observable))
        if event == 'updated':  # input value updated
            self.queued = True
            self.transferer(self.inputs, self, self.trans_arg)
            if (self.__working_value is not None) or (not self.targets):
                # Set current value
                self.queued = False
        elif event == 'completed':  # target completed transaction
            # Check whether all inputs are updated
            self.queued = any([n.queued for n in self.targets])
        else:
            pass

    def __set__current_value(self) -> None:
        value = self.__working_value
        if not value:
            return

        if self._append_values:
            self.__current_value.append(value)
        else:
            self.__current_value = value
        self.__working_value = None  # Reset working value

    def __del__(self) -> None:
        if self.verbose:
            print('Del called on node #%d' % self.id)
        self.active = False  # For possible reentrancy
        for src in self.inputs:
            if self in src.targets:
                src.targets.remove(self)  # Remove node from target list
        self.net.nodes.discard(self)  # De-register from network


class Signal(sig.Signal):
    def __init__(self, node: Node) -> None:
        self.node: Node = node
        self.notify = lambda *args: args

    def map(self, f: Callable, format_spec: str = None) -> Signal:
        if not callable(f):
            value = f

            # close scope
            def always(_):
                return value
            if format_spec is None:
                format_spec = '{}->' + str(value)
            f = always
        else:
            if format_spec is None:
                format_spec = f.__name__ + '({})'
        return self.mapn(f=f, format_spec=format_spec)

    def map2(self, other: Any, f: Callable, format_spec: str = None) -> Signal:
        # Mess with format spec and input nodes
        return self.mapn(other, f=f, format_spec=format_spec)

    def mapn(*args: Union[Signal, Any, ...], f: Callable = None, format_spec: str = None) -> Signal:
        # Mess with format spec and input nodes
        return args[0].__apply_transfer(*args[1:],
                                        trans_fun=transfer.mapn,
                                        trans_arg=f,
                                        format_spec=format_spec)

    def merge(*args: Signal) -> Signal:
        format_spec = '(' + ' ~ '.join(['{}'] * len(args)) + ')'  # e.g. ({} ~ {} ~ {})
        kwargs = {'trans_fun': transfer.merge, 'format_spec': format_spec}
        return args[0].__apply_transfer(*args[1:], **kwargs)

    def __apply_transfer(*args: Union[Signal, Any],
                         trans_fun: transferer = transfer.identity,
                         trans_arg: Optional[Callable] = None,
                         format_spec: str) -> Signal:
        net = args[0].node.net
        inps = tuple(net.get_nodes(args))
        assert len(set([n.net.id for n in inps])) == 1  # TODO move to get_nodes
        node = sig.node.Node(net, srcs=inps, trans_fun=trans_fun,
                             trans_arg=trans_arg, format_spec=format_spec)
        # TODO set format spec of node
        return sig.node.Signal(node)

    def on_value(self, f: Callable) -> Callable:
        # @fixme handle not returned
        self.node.targets.append(self)  # TODO make private; fixme make copy?
        self.notify = lambda n, _: f(n.value)  # @todo only one on_value allowed?
        return lambda: self.node.targets.remove(self)

    def output(self) -> Callable:
        return self.on_value(print)

    def to(self, other: Signal) -> Signal:
        p = self.__apply_transfer(other, trans_fun=transfer.latch, format_spec='{}.to({})')
        p.node.value = False
        return p

    def __repr__(self) -> str:
        return self.node.name()

    def __del__(self) -> None:
        if hasattr(self, 'node'):
            del self.node


class OriginSignal(Signal):
    def post(self, v: Any) -> None:
        self.node.value = v

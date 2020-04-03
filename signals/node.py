import signals as sig
from signals import transfer


class Node:
    verbose = 0

    def __init__(self, net, srcs=None, trans_fun=transfer.identity,
                 trans_arg=None, append_values=False, format_spec=None):
        if srcs is None:
            srcs = list()
        assert net.is_valid()
        self.net = net
        self.id = net.next_free_node()
        self.__current_value = list() if append_values else None
        self.__working_value = None
        self._queued = False
        self.queued = False  # Transaction status @todo doesn't need initializing
        self.targets = list()  # List of downstream nodes
        self.inputs = srcs if isinstance(srcs, list) else [srcs]  # Ensure list
        self.display_inputs = self.inputs
        self._append_values = append_values
        self.active = True  # Flag for whether in use
        self.transferer = trans_fun
        self.trans_arg = trans_arg
        self.format_spec = format_spec
        net.register_node(self)  # Add node to network node set
        for src in self.inputs:  # Register node with targets
            src.targets.append(self)

    def is_valid(self):
        return self.active & (self.id <= self.net.size)

    def name(self):
        """Name set with format spec"""
        if self.format_spec is not None:
            child_names = [n.name() for n in self.display_inputs]
            name = self.format_spec.format(*child_names)
        else:
            child_names = str(self.display_inputs)
            name = str(self) + ' = ' + self.transferer.__name__ + '(' + child_names + ')'
        return name

    def __str__(self):
        return 'Node #{}'.format(self.id)

    @property
    def value(self):
        return self.__working_value if self.__working_value is not None else self.__current_value

    @value.setter
    def value(self, v):
        if v is None:
            return
        self.__working_value = v
        self.queued = True
        for observer in self.targets:  # Notify downstream targets of change
            observer.notify(self, 'updated')

    @property
    def queued(self):
        return self._queued

    @queued.setter
    def queued(self, tf):
        if tf:
            self._queued = True
        if self._queued and not tf:  # No longer queued
            self.__set__current_value()  # Copy working value to current
            self._queued = False
            for observer in self.inputs:  # Notify upstream targets completed
                observer.notify(self, 'completed')  # @todo record if affected

    def notify(self, observable, event):
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

    def __set__current_value(self):
        value = self.__working_value
        if not value:
            return

        if self._append_values:
            self.__current_value.append(value)
        else:
            self.__current_value = value
        self.__working_value = None  # Reset working value

    def __del__(self):
        if self.verbose:
            print('Del called on node #%d' % self.id)
        self.active = False  # For possible reentrancy
        for src in self.inputs:
            if self in src.targets:
                src.targets.remove(self)  # Remove node from target list
        self.net.nodes.discard(self)  # De-register from network


class Signal(sig.Signal):
    def __init__(self, node):
        self.node = node
        self.notify = lambda *args: args

    def map(self, f, format_spec=None):
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

    def map2(self, other, f, format_spec=None):
        # Mess with format spec and input nodes
        return self.mapn(other, f=f, format_spec=format_spec)

    def mapn(*args, f=None, format_spec=None):
        # Mess with format spec and input nodes
        return args[0].__apply_transfer(*args[1:],
                                        trans_fun=transfer.mapn,
                                        trans_arg=f,
                                        format_spec=format_spec)

    def merge(*args):
        format_spec = '(' + ' ~ '.join(['{}'] * len(args)) + ')'  # e.g. ({} ~ {} ~ {})
        kwargs = {'trans_fun': transfer.merge, 'format_spec': format_spec}
        return args[0].__apply_transfer(*args[1:], **kwargs)

    def __apply_transfer(*args, trans_fun, trans_arg=None, format_spec):
        net = args[0].node.net
        inps = net.get_nodes(args)
        assert len(set([n.net.id for n in inps])) == 1  # TODO move to get_nodes
        node = sig.node.Node(net, srcs=inps, trans_fun=trans_fun,
                             trans_arg=trans_arg, format_spec=format_spec)
        # TODO set format spec of node
        return sig.node.Signal(node)

    def on_value(self, f):
        # @fixme handle not returned
        self.node.targets.append(self)  # TODO make private; fixme make copy?
        self.notify = lambda n, _: f(n.value)  # @todo only one on_value allowed?
        return lambda: self.node.targets.remove(self)

    def output(self):
        return self.on_value(print)

    def to(self, other):
        p = self.__apply_transfer(other, trans_fun=sig.transfer.latch, format_spec='{}.to({})')
        p.node.value = False

    def __repr__(self):
        return self.node.name()

    def __del__(self):
        if hasattr(self, 'node'):
            del self.node


class OriginSignal(Signal):
    def post(self, v):
        self.node.value = v

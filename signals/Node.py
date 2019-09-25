import signals as sig
from signals import transfer


class Node:
    verbose = 0

    def __init__(self, net, srcs=None, trans_fun=transfer.identity,
                 trans_arg=None, append_values=False):
        if srcs is None:
            srcs = list()
        assert net.is_valid()
        self.net = net
        self.id = net.next_free_node()
        self.inputs = srcs if isinstance(srcs, list) else [srcs]  # Ensure list
        self._current_value = None
        self._working_value = None
        self._append_values = append_values
        self.active = True  # Flag for whether in use
        self.queued = False  # Transaction status
        self.transferer = trans_fun
        self.trans_arg = trans_arg
        self.targets = set()  # List of downstream nodes
        net.register_node(self)  # Add node to network node set
        for src in self.inputs:  # Register node with targets
            src.targets.add(self)

    def is_valid(self):
        return self.active & (self.id <= self.net.size)

    def name(self):
        """Name set with format spec"""
        return self._name()

    def __str__(self):
        return 'Node #{}'.format(self.id)

    def get_value(self):
        return self._working_value if self._working_value is not None else self._current_value

    def set_value(self, value):
        if self._append_values:
            if self._working_value is not None:
                self._working_value.append(value)
            else:
                self._working_value = [value]
        else:
            self._working_value = value
        for observer in self.targets:  # Notify downstream targets of change
            observer.notify(self, 'updated')

    def notify(self, observable, event):
        if self.verbose:
            print('{} notified of "{}" event by {}'.format(self, event, observable))
        if event == 'updated':
            self.queued = True
            self.transferer(self.inputs, self, self.trans_arg)
            self.queued = False

    def __del__(self):
        if self.verbose:
            print('Del called on node #' % self.id)
        self.active = False  # For possible reentrancy
        for src in self.inputs:
            src.targets.discard(self)  # Remove node from target list
        self.net.nodes.discard(self)  # De-register from network


class Signal(sig.Signal.Signal):
    def __init__(self, node):
        self.node = node

    def map(self, f, format_spec=None):
        return self.mapn(f=f, format_spec=format_spec)

    def map2(self, other, f, format_spec=None):
        # Mess with format spec and input nodes
        return self.mapn(other, f=f, format_spec=format_spec)

    def mapn(*args, f=None, format_spec=None):
        # Mess with format spec and input nodes
        return args[0].apply_transfer(*args[1:],
                                      trans_fun=transfer.mapn,
                                      trans_arg=f,
                                      format_spec=format_spec)

    def apply_transfer(*args, trans_fun, trans_arg, format_spec):
        net = args[0].node.net
        inps = net.get_nodes(args)
        assert len(set([n.net.id for n in inps])) == 1  # TODO move to get_nodes
        node = sig.node.Node(net, srcs=inps, trans_fun=trans_fun, trans_arg=trans_arg)
        # TODO set format spec of node
        return sig.node.Signal(node)


class OriginSignal(Signal):
    def post(self, value):
        self.node.set_value(value)

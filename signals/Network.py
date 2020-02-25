import signals as sig
networks = set()


def next_free_network():
    """Return next free network id TODO Make static method?"""
    ids = set(range(Net.MAX_NETWORKS))
    in_use = {net.id for net in networks if net.is_valid()}
    available_ids = ids.difference(in_use)
    if not available_ids:
        raise Exception('Max number of active networks reached')
    else:
        return min(available_ids)


class Net:
    """A network of nodes"""
    MAX_NETWORKS = 10

    def __init__(self, size=4000, debug=False):
        """
        Network initializer
        :param size:
        :param debug:
        """
        self.nodes = set()  # Initialize node list
        self.debug = debug  # Debug mode
        # TODO Deal with max network error better
        self.id = next_free_network()  # Find next available network
        self.active = True  # Activate network
        networks.add(self)  # Add to network list
        self.size = size  # Max number of nodes in network
        if debug:
            sig.node.Node.verbose = 1

    def is_valid(self):
        return self.active & (self.id < self.MAX_NETWORKS)

    def next_free_node(self):
        """Return next free node id"""
        ids = set(range(self.size))
        in_use = {node.id for node in self.nodes if node.active}
        available_ids = ids.difference(in_use)
        if not available_ids:
            raise Exception('Max number of active nodes reached')
        else:
            return min(available_ids)

    def origin(self, name):
        return sig.node.OriginSignal(self.root_node(name))

    def root_node(self, name=None):
        node = sig.node.Node(self)
        if name:
            node._name = name
        else:
            node._name = 'n' % node.id
        node.format_spec = node._name
        return node

    def get_nodes(self, srcs):
        """
        Return/make nodes from tuple of objects
        :param srcs: A tuple of Signal objects and/or objects to turn into root nodes
        :return: A list of nodes the length of srcs
        """
        if not isinstance(srcs, tuple):
            raise TypeError("input must be a tuple")

        def make_root(src):
            """Create root node from source and set its value"""
            node = self.root_node(name=str(src))
            node.value = src
            return node
        return [s.node if isinstance(s, sig.node.Signal) else make_root(s) for s in srcs]

    def register_node(self, node):
        self.nodes.add(node)

    def __del__(self):
        self.active = False  # Set network inactive for safety (possible re-entrancy)
        if self.debug:
            print('Deleting network {}'.format(self.id))
        for node in list(self.nodes):  # Make list copy as size of set changes each iteration
            node.__del__()
        networks.discard(self)  # Remove from list

    @staticmethod
    def delete_networks():
        print('Deleting all networks')
        for net in list(networks):  # Make list copy as size of set changes each iteration
            net.__del__()

import signals as sig
networks = set()


def next_free_network():
    """Return next free network id TODO Make static method?"""
    ids = set(range(Net.MAX_NETWORKS))
    in_use = {net.id for net in networks if net.active}
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
        Network Constructor
        :param size:
        :param debug:
        """
        self.id = next_free_network()  # Find next available network
        self.active = True  # Activate network
        networks.add(self)  # Add to network list
        self.size = size  # Max number of nodes in network
        self.debug = debug  # Debug mode
        self.nodes = set()  # Initialize node list

    def is_valid(self):
        return self.active & (self.id <= self.MAX_NETWORKS)

    def next_free_node(self):
        """Return next free node id"""
        ids = set(range(self.size))
        in_use = {node.id for node in self.nodes if node.active}
        available_ids = ids.difference(in_use)
        if not available_ids:
            raise Exception('Max number of active networks reached')
        else:
            return min(available_ids)

    def add_node(self):
        self.nodes.add(sig.node.Node(self))

    def __del__(self):
        self.active = False  # Set network inactive for safety (possible re-entrancy)
        if self.debug:
            print('Deleting network {}'.format(self.id))
        # TODO Delete nodes
        networks.remove(self)  # Remove from list

    @staticmethod
    def delete_networks():
        print('Deleting all networks')
        for net in networks:
            del net

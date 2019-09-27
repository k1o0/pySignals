import unittest
import signals as sig
from signals import Network
from random import randint


class NetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.networks = Network.networks  # Add networks array
        assert not cls.networks  # Ensure empty

    def test_create(self):
        nets = list()  # Initialize network list
        # Add new network
        nets.append(sig.Net(debug=True))
        self.assertTrue(len(self.networks) == 1, 'failed to add network to list')
        self.assertTrue(nets[0].is_valid(), 'new network not valid')
        self.assertEqual(nets[0].id, 0, 'unexpected id')
        # Add another and set size
        i = randint(1, 4000)
        nets.append(sig.Net(size=i, debug=True))  # Add with specified size
        self.assertEqual(nets[-1].size, i, 'failed to set size property')
        self.assertTrue(len(self.networks) == 2, 'failed to add network to list')
        self.assertEqual(nets[-1].id, 1, 'unexpected id')
        # Delete first net and create a new one
        nets[0].__del__()
        self.assertFalse(nets[0].is_valid(), 'failed to inactivate net on delete')
        self.assertTrue(len(self.networks) == 1, 'failed to remove network on delete')
        nets.append(sig.Net(debug=True))  # Add yet another network
        self.assertEqual(nets[0].id, nets[-1].id, 'failed to reassign inactive id')
        # Test max networks
        for i in range(sig.Net.MAX_NETWORKS-len(self.networks)-1):
            nets.append(sig.Net(debug=True))  # Add up to limit of networks

        def add_net(): nets.append(sig.Net(debug=True))
        self.assertRaises(Exception, add_net, 'failed to raise exception on max networks exceeded')

    def test_delete(self):
        net = sig.Net(debug=True)
        assert net.is_valid()
        # Add some nodes to network
        net.origin('t') + 4
        nodes = list(net.nodes)  # Copy nodes to list
        net.__del__()  # Delete our network
        self.assertFalse(net.is_valid(), 'failed to inactivate net on delete')
        self.assertFalse(net.nodes, 'failed to remove nodes on net delete')
        self.assertFalse(any(node.is_valid() for node in nodes), 'failed to delete all nodes')


    def test_root_node(self):
        name = 'root'
        node = sig.Net().root_node(name)
        self.assertTrue(node.is_valid(), 'root node not valid')
        self.assertTrue(node in node.net.nodes, 'failed to register to network')
        self.assertEqual(node.name(), name, 'failed to set name')

    def test_origin(self):
        net = sig.Net()
        assert not net.nodes
        name = 'test'
        o = net.origin(name)
        self.assertTrue(isinstance(o, sig.node.OriginSignal),
                        'expected sig.node.OriginSignal but {} returned instead'.format(''))
        self.assertEqual(str(o), name, 'failed to correctly set name')
        self.assertEqual(list(net.nodes), [o.node], 'failed to register node with network')

    def test_get_nodes(self):
        net = sig.Net()
        assert not net.nodes
        inputs = (net.origin('input'), 2, '4')
        nodes = net.get_nodes(inputs)
        self.assertTrue(all(isinstance(o, sig.node.Node) for o in nodes),
                        'not all elements are nodes')
        self.assertEqual(len(inputs), len(nodes),
                         'expected list of length {} but {} returned instead'
                         .format(len(inputs), len(nodes)))
        self.assertEqual(len(net.nodes), len(nodes), 'Not all nodes registered to network')
        self.assertRaises(TypeError, lambda: net.get_nodes(4))
        # Test value set in root node
        VALUE = 5
        node = net.get_nodes((VALUE,))[0]
        self.assertEqual(node.get_value(), VALUE, 'failed to set value')

    def tearDown(self):
        Network.Net.delete_networks()  # Delete networks
        assert not any(net.is_valid() for net in Network.networks)


if __name__ == '__main__':
    unittest.main()

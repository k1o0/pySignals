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
        nets.append(sig.Net(size=i,debug=True))  # Add with specified size
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
        # TODO Add test for delete nodes
        pass

    def test_root_node(self):
        # TODO Add test for delete nodes
        pass

    def test_origin(self):
        # TODO Add test for delete nodes
        pass

    def test_get_nodes(self):
        # TODO Add test for delete nodes
        pass

    def tearDown(self):
        Network.Net.delete_networks()  # Delete networks


if __name__ == '__main__':
    unittest.main()

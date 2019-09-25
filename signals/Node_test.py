import unittest
import signals as sig
from random import randint


class NodeTest(unittest.TestCase):
    def test_create(self):
        nodes = list()  # Initialize network list
        SIZE = 5  # Set max number of nodes to low number for testing
        self.net.size = SIZE
        def add_node(): nodes.append(sig.node.Node(self.net))
        # Add new network
        add_node()
        self.assertTrue(self.net.nodes.__contains__(nodes[0]),
                        'failed to register node with network')
        self.assertTrue(nodes[0].is_valid(), 'new node not valid')
        self.assertEqual(nodes[0].id, 0, 'unexpected id')
        # Add another and set size
        add_node()
        self.assertTrue(len(self.net.nodes) == 2, 'failed to register node with network')
        self.assertEqual(nodes[-1].id, 1, 'unexpected id')
        # Delete first net and create a new one TODO move to del test
        nodes[0].__del__()
        self.assertFalse(nodes[0].is_valid(), 'failed to inactivate node on delete')
        self.assertTrue(len(self.net.nodes) == 1, 'failed to remove node on delete')
        add_node()  # Add yet another node
        self.assertEqual(nodes[0].id, nodes[-1].id, 'failed to reassign inactive id')
        # Test setting inputs and transferer
        f = sig.transfer.mapn  # Set a function to set
        i = randint(1, 4000)
        n = nodes[-1:-2]
        nodes.append(sig.node.Node(self.net, srcs=n, trans_fun=f, trans_arg=i, append_values=True))
        self.assertTrue(nodes[-1]._append_values, 'failed to set append_values flag')
        self.assertEqual(nodes[-1].trans_arg, i, 'failed to set trans_arg')
        self.assertEqual(nodes[-1].transferer, f, 'failed to set transferer')
        self.assertEqual(nodes[-1].inputs, n, 'failed to set inputs')
        # Check target registration
        for node in nodes[-1].inputs:
            self.assertTrue(node.targets.__contains__(nodes[-1]), 'failed to register target')
        # Test creating with single input
        nodes.append(sig.node.Node(self.net, srcs=nodes[-1]))
        self.assertTrue(isinstance(nodes[-1].inputs, list), 'failed to add single input as list')
        # Test max networks
        for i in range(SIZE-len(nodes)-1):
            add_node()  # Add up to limit of nodes
        self.assertRaises(Exception, add_node, 'failed to raise exception on max nodes exceeded')
        # Test creation with invalid network
        self.net.active = False  # Inactivate network
        self.assertRaises(Exception, add_node, 'failed to raise exception on invalid network')

    def test_set_values(self):
        # Test setting values
        node = sig.node.Node(self.net)  # Create node
        self.assertEqual(node.get_value(), None, 'expected None for value of new node')
        # Set a value
        i = randint(0, 10000)
        node.set_value(i)
        self.assertEqual(node.get_value(), i, 'expected None for value of new node')
        # Set another value
        i = randint(0, 10000)
        node.set_value(i)
        self.assertEqual(node.get_value(), i, 'expected None for value of new node')
        # Test appending values
        node = sig.node.Node(self.net, append_values=True)  # Create new node
        i = randint(0, 10000)
        node.set_value(i)  # Set a couple of values
        node.set_value(i)
        actual = node.get_value()
        expected = (len(actual) == 2) & (actual[-1] == i)
        self.assertTrue(expected, 'failed to append values')

    def test_get_values(self):
        node = sig.node.Node(self.net)  # Create node
        self.assertEqual(node.get_value(), None, 'expected None for value of new node')
        node._current_value = 5
        self.assertEqual(node.get_value(), node._current_value, 'failed to return current value')
        node._working_value = 3
        self.assertEqual(node.get_value(), node._working_value, 'failed to return working value')

    def test_transferer(self):
        # Test transfer function is called
        o = sig.node.Node(self.net)
        called = list()  # Object whose state we can modify
        def f(*args): args[2].append(True)  # Update `called` variable
        sig.node.Node(self.net, srcs=o, trans_fun=f, trans_arg=called)  # Create new node
        assert not called  # Ensure evaluates False
        o.set_value(4)
        self.assertTrue(called, 'failed to call transfer function')

    @unittest.skip('Not ready yet')
    def test_format_spec(self):
        pass

    @unittest.skip('Not ready yet')
    def test_delete_node(self):
        pass

    def setUp(self):
        self.net = sig.Network.Net()
        assert not self.net.nodes

    def tearDown(self):
        del self.net


if __name__ == '__main__':
    unittest.main()

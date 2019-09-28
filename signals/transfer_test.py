import unittest
import signals as sig
import numpy as np


class TransfererTest(unittest.TestCase):
    def test_identity(self):
        VALUE = 5
        a = self.net.get_nodes([VALUE])
        out = sig.node.Node(self.net, srcs=a, trans_fun=sig.transfer.identity)
        assert not out.get_value()  # Ensure no value set
        sig.transfer.identity(a, out, None)
        self.assertEqual(out.get_value(), VALUE, 'failed to update node value')

    def test_mapn(self):
        VALUE = 5
        a = sig.node.Node(self.net)
        out = sig.node.Node(self.net, srcs=a)
        assert not out.get_value() and not a.get_value()  # Ensure no values set
        sig.transfer.mapn([a], out, np.square)  # Call with unset values
        self.assertEqual(out.get_value(), None, 'unexpected node value')
        a._current_value = VALUE  # Set value
        sig.transfer.mapn([a], out, np.square)  # Call with set values
        self.assertEqual(out.get_value(), VALUE**2, 'failed to update node value')

    @unittest.skip('Not ready yet')
    def test_latch(self):
        pass

    def setUp(self):
        self.net = sig.Network.Net()
        assert not self.net.nodes


if __name__ == '__main__':
    unittest.main()

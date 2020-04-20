import unittest
import numpy as np
import signals as sig


class TransfererTest(unittest.TestCase):
    def test_identity(self):
        VALUE = 5
        a = tuple(self.net.get_nodes((VALUE,)))
        out = sig.node.Node(self.net, srcs=a, trans_fun=sig.transfer.identity)
        assert not out.value  # Ensure no value set
        sig.transfer.identity(a, out, None)
        self.assertEqual(out.value, VALUE, 'failed to update node value')

    def test_mapn(self):
        VALUE = 5
        a = sig.node.Node(self.net)
        out = sig.node.Node(self.net, srcs=a)
        assert not out.value and not a.value  # Ensure no values set
        sig.transfer.mapn((a,), out, np.square)  # Call with unset values
        self.assertEqual(out.value, None, 'unexpected node value')
        a.value = VALUE  # Set value
        sig.transfer.mapn((a,), out, np.square)  # Call with set values
        self.assertEqual(out.value, VALUE**2, 'failed to update node value')

    def test_merge(self):
        VALUE = 5
        a = sig.node.Node(self.net)
        b = sig.node.Node(self.net)
        out = sig.node.Node(self.net, srcs=a)
        assert not out.value and not a.value  # Ensure no values set
        sig.transfer.merge((a, b), out, None)  # Call with unset values
        self.assertEqual(out.value, None, 'unexpected node value')
        b.value = VALUE  # Set value
        sig.transfer.merge((a, b), out, None)  # Call with set values
        self.assertEqual(out.value, VALUE, 'failed to update node value')

    @unittest.skip('Not ready yet')
    def test_latch(self):
        pass

    def setUp(self):
        self.net = sig.network.Net()
        assert not self.net.nodes


if __name__ == '__main__':
    unittest.main()

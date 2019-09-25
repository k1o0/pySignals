import unittest
import signals as sig


class SignalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.net = sig.Net()
        cls.origin = cls.net.origin('input')

    @unittest.skip('Not ready yet')
    def test_add(self):
        s = self.origin + 2
        # TODO Test format spec
        self.origin.post(2)
        self.assertEqual(s.node.get_value(), 4)

    @unittest.skip('Not ready yet')
    def test_sub(self):
        s = self.origin + 5
        # TODO Test format spec
        self.origin.post(2)
        self.assertEqual(s.node.get_value(), 3)


if __name__ == '__main__':
    unittest.main()

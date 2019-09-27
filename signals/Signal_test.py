import unittest
import signals as sig


class SignalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.net = sig.Net()
        cls.origin = cls.net.origin('input')

    def test_add(self):
        s = self.origin + 2
        self.assertEqual(s.__repr__(), 'input + 2', 'failed to correctly format representation')
        self.origin.post(2)
        self.assertEqual(s.node.get_value(), 4, 'incorrect value')

    def test_sub(self):
        s = self.origin - 3
        self.assertEqual(s.__repr__(), 'input - 3', 'failed to correctly format representation')
        self.origin.post(5)
        self.assertEqual(s.node.get_value(), 2, 'incorrect value')


if __name__ == '__main__':
    unittest.main()

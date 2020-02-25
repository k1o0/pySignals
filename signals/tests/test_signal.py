import unittest
import signals as sig
import random


class SignalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.net = sig.Net()
        cls.origin = cls.net.origin('input')

    def test_add(self):
        s = self.origin + 2
        self.assertEqual(s.__repr__(), 'input + 2', 'failed to correctly format representation')
        self.origin.post(2)
        self.assertEqual(s.node.value, 4, 'incorrect value')

    def test_sub(self):
        s = self.origin - 3
        self.assertEqual(s.__repr__(), 'input - 3', 'failed to correctly format representation')
        self.origin.post(5)
        self.assertEqual(s.node.value, 2, 'incorrect value')

    def test_gt(self):
        s = self.origin > 3
        self.assertEqual(s.__repr__(), 'input > 3', 'failed to correctly format representation')
        self.origin.post(5)
        self.assertTrue(s.node.value, 'incorrect value')
        self.origin.post(3)
        self.assertFalse(s.node.value, 'incorrect value')
        # TODO test arrays

    def test_on_value(self):
        s = self.origin
        actual = list()
        unsub = s.on_value(lambda x: actual.append(x))
        expected = random.sample(range(10000), 5)
        for val in expected:
            self.origin.post(val)
        self.assertEqual(actual, expected, 'failed to call function on update')
        # Test unsub:
        unsub()
        self.origin.post(5)
        self.assertEqual(actual, expected, 'failed unsub observer')

    @unittest.skip('Not ready yet')
    def test_output(self):
        pass

    @unittest.skip('Not ready yet')
    def test_to(self):
        pass


if __name__ == '__main__':
    unittest.main()

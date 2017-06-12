import unittest
from zproj.peeker import Peeker

class TestEmptyPeeker(unittest.TestCase):

    def setUp(self):
        self._pkr = Peeker([])

    def test_empty_bool(self):
        self.assertFalse(self._pkr)

    def test_empty_peek(self):
        """Test behavior of peek for Peeker on empty iterable."""
        for i in range(2):
            with self.assertRaises(IndexError):
                self._pkr.peek(i)

    def test_empty_advance(self):
        """Test behavior of advance for Peeker on empty iterable."""
        self._pkr.advance(0)
        with self.assertRaises(IndexError):
            self._pkr.advance(1)


class TestNonemptyPeeker(unittest.TestCase):

    def test_iteration(self):
        itr = range(10)
        pkr = Peeker(itr)
        itr_list = []
        for i in range(10):
            itr_list.append(pkr.peek(0))
            pkr.advance(1)
        with self.assertRaises(IndexError):
            pkr.advance(1)
        self.assertEqual(itr_list, list(itr))

    def test_multiple_advances(self):
        n = 10
        itr = range(n)
        pkr = Peeker(itr)
        for i in range(n - 1):
            pkr.advance(1)
        # pkr.advance(n - 1)
        self.assertEqual(pkr.peek(0), n - 1)

    def test_bool(self):
        pkr = Peeker([1])
        self.assertTrue(pkr)
        pkr.advance(1)
        self.assertFalse(pkr)

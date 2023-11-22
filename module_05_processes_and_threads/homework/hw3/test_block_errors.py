import unittest
from block_errors import BlockErrors

class TestBlockError(unittest.TestCase):
    def test_error_blocked(self):
        err_types = {ZeroDivisionError, TypeError}
        with BlockErrors(err_types):
            a = 1 / 0
        self.assertTrue(True)

    def test_error_not_blocked(self):
        with self.assertRaises(TypeError):
            err_types = {ZeroDivisionError}
            with BlockErrors(err_types):
                a = 1 / '0'

    def test_outer_block_no_errors(self):
        outer_err_types = {TypeError}
        with BlockErrors(outer_err_types):
            inner_err_types = {ZeroDivisionError}
            with BlockErrors(inner_err_types):
                a = 1 / '0'
        self.assertTrue(True)

    def test_global_error_supression(self):
        err_types = {Exception}
        with BlockErrors(err_types):
            a = 1 / '0'

if __name__ == '__main__':
    unittest.main()

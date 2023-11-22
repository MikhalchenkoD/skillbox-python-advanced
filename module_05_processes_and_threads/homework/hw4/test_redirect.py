from redirect import Redirect
import sys
import io
import unittest
from contextlib import redirect_stdout, redirect_stderr


class RedirectTestCase(unittest.TestCase):
    def test_redirect_stdout(self):
        stdout_mock = io.StringIO()

        with redirect_stdout(stdout_mock), Redirect(stdout=stdout_mock):
            print("Hello stdout.txt")

        captured_output = stdout_mock.getvalue().strip()
        self.assertEqual(captured_output, "Hello stdout.txt")

    def test_redirect_stderr(self):
        stderr_mock = io.StringIO()

        with redirect_stderr(stderr_mock), Redirect(stderr=stderr_mock):
            try:
                raise Exception("Hello stderr.txt")
            except Exception as e:
                print(str(e), file=sys.stderr)

        captured_output = stderr_mock.getvalue().strip()
        self.assertEqual(captured_output, "Hello stderr.txt")


if __name__ == '__main__':
    unittest.main()

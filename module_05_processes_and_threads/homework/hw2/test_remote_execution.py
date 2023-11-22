import unittest
from remote_execution import app


class TestRunCode(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()
        self.base_url = "/runcode"

    def test_will_raise_when_timeout_reached(self):
        with self.assertRaises(ValueError):
            payload = {
                "code": "from time import sleep;sleep(10)", "timeout": 1}
            self.app.post(self.base_url, data=payload)

    def test_will_validate(self):
        payload = {
            "code": "from time import sleep;sleep(10)", "timeout": 0}
        response = self.app.post(self.base_url, data=payload)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()

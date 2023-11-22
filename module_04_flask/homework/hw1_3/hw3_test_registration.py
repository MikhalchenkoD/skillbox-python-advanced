"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from hw1_registration import app


class TestValidators(unittest.TestCase):

    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.url = "/registration"
        self.app = app.test_client()
        self.args = dict(
            email='mat@mail.com', phone=9999999999,
            name="Matthew", address="EKB",
            index=33, comment='')

    def test_check_correct_email(self):
        self.args["email"] = "mat@mail.ru"
        response = self.app.post(self.url, data=self.args)
        response_data = response.get_data(as_text=True)
        self.assertIn("ОК", response_data)
        self.assertTrue(response.status_code == 200)

    def test_check_dont_have_email(self):
        self.args["email"] = ""
        response = self.app.post(self.url, data=self.args)
        response_data = response.get_data(as_text=True)
        self.assertNotIn("ОК", response_data)
        self.assertTrue(response.status_code == 400)

    def test_check_wrong_email(self):
        self.args["email"] = "matmailru"
        response = self.app.post(self.url, data=self.args)
        response_data = response.get_data(as_text=True)
        self.assertNotIn("ОК", response_data)
        self.assertTrue(response.status_code == 400)

    def test_check_correct_phone(self):
        self.args["phone"] = 7777777777
        response = self.app.post(self.url, data=self.args)
        response_data = response.get_data(as_text=True)
        self.assertIn("ОК", response_data)
        self.assertTrue(response.status_code == 200)

    def test_check_dont_have_phone(self):
        self.args["phone"] = None
        response = self.app.post(self.url, data=self.args)
        response_data = response.get_data(as_text=True)
        self.assertNotIn("ОК", response_data)
        self.assertTrue(response.status_code == 400)

    def test_check_wrong_phone(self):
        self.args["phone"] = 1234567891011
        response = self.app.post(self.url, data=self.args)
        response_data = response.get_data(as_text=True)
        self.assertNotIn("ОК", response_data)
        self.assertTrue(response.status_code == 400)

    def test_check_dont_have_name(self):
        self.args["name"] = ""
        response = self.app.post(self.url, data=self.args)
        response_data = response.get_data(as_text=True)
        self.assertNotIn("ОК", response_data)
        self.assertTrue(response.status_code == 400)

    def test_check_dont_have_address(self):
        self.args["address"] = ""
        response = self.app.post(self.url, data=self.args)
        response_data = response.get_data(as_text=True)
        self.assertNotIn("ОК", response_data)
        self.assertTrue(response.status_code == 400)

    def test_check_correct_index(self):
        self.args["index"] = 44
        response = self.app.post(self.url, data=self.args)
        response_data = response.get_data(as_text=True)
        self.assertIn("ОК", response_data)
        self.assertTrue(response.status_code == 200)

    def test_check_dont_have_index(self):
        self.args["index"] = None
        response = self.app.post(self.url, data=self.args)
        response_data = response.get_data(as_text=True)
        self.assertNotIn("ОК", response_data)
        self.assertTrue(response.status_code == 400)

    def test_check_wrong_index(self):
        self.args["index"] = "matmailru"
        response = self.app.post(self.url, data=self.args)
        response_data = response.get_data(as_text=True)
        self.assertNotIn("ОК", response_data)
        self.assertTrue(response.status_code == 400)


if __name__ == '__main__':
    unittest.main()

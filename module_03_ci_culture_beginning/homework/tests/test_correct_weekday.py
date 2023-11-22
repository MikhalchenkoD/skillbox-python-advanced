import unittest
from freezegun import freeze_time
from python_advanced.module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app


class TestCorrectWeekday(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()
        self.base_url = '/hello-world/'

    @freeze_time("2023-04-29")
    def test_can_get_correct_weekdate_tomorrow(self):
        username = "Dmitry"
        greeting = "Хорошей субботы!"
        response = self.app.get(self.base_url + username)
        response_text = response.data.decode()
        self.assertTrue(greeting in response_text)

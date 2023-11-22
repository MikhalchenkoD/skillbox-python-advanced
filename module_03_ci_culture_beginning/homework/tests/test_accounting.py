import unittest
from python_advanced.module_02_linux.homework.hw7.accounting import app


class TestAccountingOfFinances(unittest.TestCase):
    def setUp(self) -> None:
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        self.app = app.test_client()

    def test_endpoint_add(self):
        date = "20230202"
        summ = "800"
        url = "/add/" + date + "/" + summ
        response = self.app.get(url)
        response_data = response.data.decode()
        self.assertTrue("1600" in response_data)

    def test_endpoint_calculate_month(self):
        year = "2023"
        month = "02"
        url = "/calculate/" + year + "/" + month
        response = self.app.get(url)
        response_data = response.data.decode()
        self.assertTrue("3400" in response_data)

    def test_endpoint_calculate_year(self):
        year = "2023"
        url = "/calculate/" + year
        response = self.app.get(url)
        response_data = response.data.decode()
        self.assertTrue("4900" in response_data)

    def test_invalid_data_in_endpoint_add(self):
        date = "202f302f2022f"
        summ = "800"
        url = "/add/" + date + "/" + summ
        try:
            response = self.app.get(url)
        except:
            self.assertRaises(ValueError)

import unittest
from python_advanced.module_03_ci_culture_beginning.homework.hw4.person import Person


class TestTrustFunction(unittest.TestCase):

    def setUp(self) -> None:
        self.Person = Person("Matvey", 2003, "Gubakha")

    def test_get_name(self):
        try:
            value = self.Person.__name
        except Exception as exp:
            self.assertRaises(type(exp))

    def test_get_address(self):
        try:
            value = self.Person.__address
        except Exception as exp:
            self.assertRaises(type(exp))

    def test_correct_get_age(self):
        self.assertTrue(self.Person.get_age() > 0)

    def test_set_name(self):
        try:
            self.Person.name = "Andrey"
        except Exception as exp:
            self.assertRaises(type(exp))

    def test_set_address(self):
        try:
            self.Person.address = "Moskow"
        except Exception as exp:
            self.assertRaises(type(exp))

    def test_set_age(self):
        try:
            self.Person.age = 22
        except Exception as exp:
            self.assertRaises(type(exp))

    def address_is_not_none(self):
        self.assertTrue(self.Person.get_address() is not None)

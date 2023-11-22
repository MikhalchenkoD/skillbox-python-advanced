import datetime


class Person:
    def __init__(self, name, year_of_birth, address=''):
        self.__name = name
        self.__yob = year_of_birth
        self.__address = address

    def get_age(self):
        now = datetime.datetime.now()
        return now.year - self.__yob

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def set_address(self, address):
        self.__address = address

    def get_address(self):
        return self.__address

    def is_homeless(self):
        '''
        returns True if address is not set, false in other case
        '''
        return self.__address is None

import factory
import factory.fuzzy as fuzzy
import random

from factory import LazyAttribute

from ..api.main import db
from ..api.models import Client, Parking


class ClientFactory(factory.Factory):
    class Meta:
        model = Client

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = factory.Faker('text')
    car_number = factory.Faker('text')


class ParkingFactory(factory.Factory):
    class Meta:
        model = Parking

    address = factory.Faker('address')
    opened = factory.Faker('boolean')
    count_places = factory.Faker('random_int')
    count_available_places = LazyAttribute(
        lambda obj: obj.count_places - 1)

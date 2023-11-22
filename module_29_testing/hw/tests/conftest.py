import datetime

import pytest
from ..api.main import create_app, db as _db
from ..api.models import Client, Parking, ClientParking

@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        client1 = Client(
                        name="name",
                        surname="surname",
                        credit_card='credit_card',
                        car_number='car_number')

        client2 = Client(
                        name="name2",
                        surname="surname2",
                        credit_card='credit_card2',
                        car_number='car_number2')

        parking = Parking(address="address",
                          opened=True,
                          count_places=5,
                          count_available_places=5)

        client_parking = ClientParking(client_id=1,
                                       parking_id=1,
                                       time_in=datetime.datetime.now(),
                                       time_out=datetime.datetime.now())

        _db.session.add(client1)
        _db.session.add(client2)
        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db

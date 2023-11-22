from .factories import ClientFactory, ParkingFactory
from ..api.models import Client, Parking


def test_create_client_with_factory(app, db):
    client = ClientFactory()

    db.session.add(client)
    db.session.commit()

    assert client.id is not None
    assert len(db.session.query(Client).all()) == 3


def test_create_parking_with_factory(client, db):
    parking = ParkingFactory()

    db.session.add(parking)
    db.session.commit()

    assert parking.id is not None
    assert len(db.session.query(Parking).all()) == 2

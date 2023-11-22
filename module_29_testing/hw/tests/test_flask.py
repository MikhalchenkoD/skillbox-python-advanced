import json
import pytest


@pytest.mark.parametrize("route", ["/client", "/client/1"])
def test_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200


def test_create_client(client) -> None:
    client_data = {"name": "Никита", "surname": "Нестеренко",
                   "credit_card": "credit_card", "car_number": "car_number"}
    resp = client.post("/client", data=client_data)

    assert resp.status_code == 200


def test_create_parking(client) -> None:
    parking_data = {"address": "address", "opened": True,
                    "count_places": 5, "count_available_places": 5}
    resp = client.post("/parkings", data=parking_data)

    assert resp.status_code == 200


@pytest.mark.parking
def test_create_client_parking(client) -> None:
    client_parking_data = {"client_id": 2, "parking_id": 1}
    resp = client.post("/client_parkings", data=client_parking_data)

    assert resp.status_code == 200


@pytest.mark.parking
def test_delete_client_parking(client) -> None:
    client_parking_data = {"client_id": 1, "parking_id": 1}
    resp = client.delete("/client_parkings", data=client_parking_data)

    assert resp.status_code == 200
    assert resp.json["time_in"] <= resp.json["time_out"]

import datetime

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from typing import List

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///parking.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import Client, ClientParking, Parking

    @app.before_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route('/client', methods=['GET'])
    def get_all_clients():
        clients = db.session.query(Client).all()
        clients_list = [u.to_json() for u in clients]

        return jsonify(clients_list), 200

    @app.route('/client/<int:client_id>', methods=['GET'])
    def get_client_by_id(client_id):
        client = db.session.query(Client).get(client_id)

        return jsonify(client.to_json()), 200

    @app.route('/client', methods=['POST'])
    def create_new_client():
        name = request.form.get('name')
        surname = request.form.get('surname')
        credit_card = request.form.get('credit_card')
        car_number = request.form.get('car_number')

        new_client = Client(name=name,
                            surname=surname,
                            credit_card=credit_card,
                            car_number=car_number)

        db.session.add(new_client)
        db.session.commit()

        return jsonify(new_client.to_json()), 200

    @app.route('/parkings', methods=['POST'])
    def create_new_parking():
        address = request.form.get('address')
        count_places = request.form.get('count_places')
        count_available_places = request.form.get('count_available_places')
        opened = request.form.get('opened', type=bool)

        new_parking = Parking(address=address,
                              count_places=count_places,
                              count_available_places=count_available_places,
                              opened=opened)

        db.session.add(new_parking)
        db.session.commit()

        return jsonify(new_parking.to_json()), 200

    @app.route('/client_parkings', methods=['POST'])
    def create_new_client_parking():
        client_id = request.form.get('client_id', type=int)
        parking_id = request.form.get('parking_id', type=int)

        parking = db.session.query(Parking).get(parking_id)

        if not parking.opened or parking.count_available_places == 0:
            return 'Парковка закрыта или нет свободных мест', 403

        parking.count_available_places -= 1

        time_in = datetime.datetime.now()

        client_parking = ClientParking(client_id=client_id,
                                       parking_id=parking_id,
                                       time_in=time_in)

        db.session.add(client_parking)
        db.session.commit()

        return jsonify(client_parking.to_json()), 200

    @app.route('/client_parkings', methods=['DELETE'])
    def delete_client_parking():
        client_id = request.form.get('client_id', type=int)
        parking_id = request.form.get('parking_id', type=int)

        parking = db.session.query(Parking).get(parking_id)
        parking.count_available_places += 1

        client = db.session.query(Client).get(client_id)

        if not client.credit_card:
            return 'Сначала оплатите парковку', 403

        client_parking = db.session.query(ClientParking).get(client_id)

        time = datetime.datetime.now()
        client_parking.time_out = time

        db.session.delete(client_parking)
        db.session.commit()

        return jsonify(client_parking.to_json()), 200

    return app

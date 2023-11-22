import requests
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String, Boolean, JSON, ForeignKey, ARRAY, func, text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

app = Flask(__name__)

engine = create_engine('postgresql+psycopg2://admin:admin@postgres/skillbox_db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Coffee(Base):
    __tablename__ = 'coffee'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(200), nullable=False)
    origin = Column(String(200))
    intensifier = Column(String(100))
    notes = Column(ARRAY(String))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(50), nullable=False)
    has_sale = Column(Boolean)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey('coffee.id'))

    coffee = relationship("Coffee", backref="users")


def get_random_address():
    response = requests.get("https://random-data-api.com/api/address/random_address")
    data = response.json()
    return data.get('address', {})


def create_random_coffee():
    response = requests.get("https://random-data-api.com/api/coffee/random_coffee")
    data = response.json()
    coffee = Coffee(
        title=data.get('blend_name'),
        origin=data.get('origin'),
        notes=data.get('notes'),
        intensifier=data.get('intensifier')
    )
    return coffee


@app.before_request
def before_first_request():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    for _ in range(10):
        address = get_random_address()
        user = User(
            name="Name",  # Замените на случайное имя или как вам удобно генерировать
            has_sale=True,
            address=address
        )
        session.add(user)

    for _ in range(10):
        coffee = create_random_coffee()
        session.add(coffee)

    session.commit()
    session.close()


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get('name')
    country = data.get('country')

    user = User(name=name, address={"country": country})
    session.add(user)
    session.commit()
    session.close()

    return jsonify({'message': 'User added successfully'})


@app.route('/coffee_by_name', methods=['GET'])
def coffee_by_name():
    coffee_name = request.args.get('name')

    coffees = session.query(Coffee).filter(Coffee.title.ilike(f'%{coffee_name}%')).all()
    session.close()

    return jsonify([coffee.__dict__ for coffee in coffees])


@app.route('/unique_notes', methods=['GET'])
def unique_notes():
    unique_notes = session.query(func.unnest(Coffee.notes).label("note")).distinct().all()
    session.close()

    return jsonify([note.note for note in unique_notes])


@app.route('/users_by_country', methods=['GET'])
def users_by_country():
    country = request.args.get('country')

    users = session.query(User).filter(text("address ->> 'country' = :country")).params(country=country).all()
    session.close()

    return jsonify([user.__dict__ for user in users])

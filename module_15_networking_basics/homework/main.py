import datetime

from flask import Flask, request, Response, jsonify

from models import init_db, Room, add_room_to_db, get_rooms, get_all_rooms, Order, add_order, get_order

app: Flask = Flask(__name__)

@app.route('/add-room', methods=['POST'])
def add_room() -> Response:
    if request.method == "POST":
        data = request.get_json()
        room = Room(
            id=None,
            floor=data["floor"],
            beds=data["beds"],
            guestNum=data["guestNum"],
            price=data["price"]
        )
        add_room_to_db(room)
        return jsonify({"id": room.id}), 201  # Return id and status code 201

@app.route('/get-rooms', methods=['GET'])
def get_room() -> Response:
    if request.args.get('checkIn') and request.args.get('checkOut'):
        rooms = get_rooms(request.args.get('checkIn'), request.args.get('checkOut'))
    else:
        rooms = get_rooms()
    properties: dict = {}
    properties["rooms"] = []
    for room in rooms:
        properties["rooms"].append({
            "roomId": room.id,
            "floor": room.floor,
            "beds": room.beds,
            "guestNum": room.guestNum,
            "price": room.price,
            "bookingParams": {
                "checkIn": request.args.get('checkIn'),
                "checkOut": request.args.get('checkOut'),
                "roomId": room.id
            }
        })
    return jsonify(properties)

@app.route('/get-rooms-len', methods=['GET'])
def get_all_rooms_len() -> Response:
    rooms = get_all_rooms()
    properties: dict = {}
    properties["rooms"] = []
    for room in rooms:
        properties["rooms"].append({
            "roomId": room.id,
            "floor": room.floor,
            "beds": room.beds,
            "guestNum": room.guestNum,
            "price": room.price
        })
    return jsonify(properties)



@app.route('/book-room', methods=['POST'])
def booking():
    if request.method == "POST":
        data = request.get_json()
        checkIn = datetime.datetime.strptime(str(data["bookingDates"]["checkIn"]), "%Y%m%d")
        checkOut = datetime.datetime.strptime(str(data["bookingDates"]["checkOut"]), "%Y%m%d")
        order = Order(
            id=None,
            checkIn=checkIn,
            checkOut=checkOut,
            firstName=data["firstName"],
            lastName=data["lastName"],
            roomId=data["roomId"]
        )
        if get_order(order):
            return Response(status=409)
        order_id = add_order(order)
        return jsonify({"roomId": order_id}), 201  # Return id and status code 201

if __name__ == '__main__':
    init_db()
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True, port=5000, host="127.0.0.1")

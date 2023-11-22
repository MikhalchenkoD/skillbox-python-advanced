import datetime
import sqlite3
from typing import Optional, Any


class Room:
    def __init__(self, id: Optional[int], floor: int, beds: int, guestNum: int, price: int):
        self.id: int = id
        self.floor: int = floor
        self.beds: int = beds
        self.guestNum: int = guestNum
        self.price: int = price

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

class Order:

    def __init__(self, id: Optional[int], checkIn: datetime, checkOut: datetime, firstName: str, lastName: str, roomId: int):
        self.id = id
        self.checkIn: datetime = checkIn
        self.checkOut: datetime = checkOut
        self.firstname = firstName
        self.lastName = lastName
        self.roomId = roomId

def init_db() -> None:
    with sqlite3.connect('table_room.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS `table_rooms` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    floor INTEGER, 
                    beds INTEGER,
                    guestNum INTEGER,
                    price INTEGER
                );
            """
        )
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS `table_orders` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    checkIn DATETIME,
                    checkOut DATETIME,
                    firstName VARCHAR(255),
                    lastName VARCHAR(255),
                    roomId INTEGER,
                    FOREIGN KEY (roomId) REFERENCES table_rooms(id))
            """
        )


def add_room_to_db(room: Room):
    with sqlite3.connect('table_room.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        query = f"""
                  INSERT INTO table_rooms (floor, beds, guestNum, price) VALUES 
                  (?, ?, ?, ?)
                      """
        cursor.execute(query, (room.floor, room.beds, room.guestNum, room.price))
        conn.commit()


def add_order(order: Order):
    with sqlite3.connect('table_room.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        query = """
            INSERT INTO `table_orders` (checkIn, checkOut, firstName, lastName, roomId) VALUES 
            (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (order.checkIn, order.checkOut, order.firstName, order.lastName, order.roomId))
        conn.commit()

        # Получить последний добавленный id
        cursor.execute("SELECT last_insert_rowid();")
        order_id = cursor.fetchone()[0]

        return order_id


def get_order(order: Order):
    with sqlite3.connect('table_room.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        query = """
            SELECT * FROM `table_orders` WHERE checkIn >= ? AND checkIn <= ? AND roomId = ?;
        """
        cursor.execute(query, (order.checkIn, order.checkOut, order.roomId))
        orders = [Order(*row) for row in cursor.fetchall()]
        return orders

def get_all_rooms():
    with sqlite3.connect('table_room.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM `table_rooms`
            """
        )
        return [Room(*row) for row in cursor.fetchall()]



def get_rooms(checkIn: str = None, checkOut: str = None) -> list[Room]:
    with sqlite3.connect('table_room.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
                """
                SELECT * from `table_rooms`
                """
            )
        return [Room(*row) for row in cursor.fetchall()]
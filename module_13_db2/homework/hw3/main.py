import datetime
import sqlite3

sql_request_check_availability_in_table = """
SELECT EXISTS(SELECT * FROM 'birds' WHERE bird_name = ?)
"""

sql_request_add_bird = """ INSERT INTO 'birds' (bird_name, time) VALUES (?, ?);
"""

def log_bird(
        cursor: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    cursor.execute(sql_request_add_bird, (bird_name, date_time))
    print(f"Птица {bird_name} записана в журнал")

def check_if_such_bird_already_seen(
        cursor: sqlite3.Cursor,
        bird_name: str
) -> bool:
    cursor.execute(sql_request_check_availability_in_table, (bird_name,))
    res = cursor.fetchone()
    return res[0]


if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor = conn.cursor()
        bird_name = input("Введите птицу\n").lower()
        if not check_if_such_bird_already_seen(cursor, bird_name):
            log_bird(cursor, bird_name, str(datetime.datetime.now().time()))
        else:
            print(f"{bird_name} уже есть в таблице")
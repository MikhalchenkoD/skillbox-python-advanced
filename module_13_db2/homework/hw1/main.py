import sqlite3

sql_request = """SELECT * FROM 'table_truck_with_vaccine'
WHERE temperature_in_celsius NOT BETWEEN 16 AND 20 AND truck_number = ? ORDER BY timestamp
"""

def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    cursor.execute(sql_request, (truck_number,))
    res_sql = cursor.fetchall()
    print(res_sql)
    if len(res_sql) >= 3:
        return True
    return False

if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor = conn.cursor()
        truck_number = input("Введите номер грузовика:\n")
        if check_if_vaccine_has_spoiled(cursor, truck_number):
            print("Вакцина испортилась")
        else:
            print("Вакцина НЕ испортилась")
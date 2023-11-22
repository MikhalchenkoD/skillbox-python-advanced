import sqlite3
import csv

sql_request = """ DELETE FROM 'table_fees'
WHERE truck_number = ? AND timestamp = ?
"""

def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    with open(wrong_fees_file) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        for row in spamreader:
            cursor.execute(sql_request, (row[0], row[1]))

if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
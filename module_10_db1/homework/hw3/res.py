import sqlite3
with sqlite3.connect("hw_3_database.db") as conn:
    cursor = conn.cursor()
    for i in range(1, 4):
        cursor.execute(f"SELECT COUNT(table_{i}.id) FROM `table_{i}`")
        result = cursor.fetchall()
        print(f"Записей в {i} таблице:", result[0][0])
    cursor.execute(f"SELECT COUNT(DISTINCT VALUE) FROM `table_1`")
    result = cursor.fetchall()
    print("Уникальных записей в таблице 1:", result[0][0])
    cursor.execute(f"SELECT table_1.value FROM 'table_1' INTERSECT SELECT table_2.value FROM 'table_2'")
    result = cursor.fetchall()
    print("Количество записей из таблицы 1, встречающихся в таблице 2:", len(result))
    cursor.execute(f"SELECT table_1.value FROM 'table_1' INTERSECT SELECT table_2.value FROM 'table_2'"
                   f"INTERSECT SELECT table_3.value FROM 'table_3'")
    result = cursor.fetchall()
    print("Количество записей из таблицы 1, встречающихся в таблицах 2 и 3:", len(result))



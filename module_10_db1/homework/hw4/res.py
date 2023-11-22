import sqlite3
import math
with sqlite3.connect("hw_4_database.db") as conn:
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM `salaries` WHERE salaries.salary < 5000")
    result = cursor.fetchall()
    print("Число жителей, находящихся за чертой бедности:", result[0][0])


    cursor.execute(f"SELECT AVG(salaries.salary) FROM `salaries`")
    result = cursor.fetchall()
    print("Средняя зп:", result[0][0])


    cursor.execute(f"SELECT salary FROM salaries ORDER BY salary "
                             f"LIMIT 1 OFFSET (SELECT COUNT(*) FROM salaries) / 2")
    result = cursor.fetchall()
    print("Медианная зп:", result[0][0])


    cursor.execute("SELECT COUNT(salary) FROM salaries")
    TOTAL = cursor.fetchone()[0]
    cursor.execute(f"SELECT SUM(salary) FROM (SELECT * FROM salaries ORDER BY salary DESC LIMIT 0.1 * {TOTAL})")
    TOP10 = cursor.fetchone()[0]
    cursor.execute(f"SELECT SUM(salary) FROM (SELECT * FROM salaries ORDER BY salary ASC LIMIT 0.9 * {TOTAL})")
    NOTOP10 = cursor.fetchone()[0]
    print("Число социального неравенства F:", round(TOP10/NOTOP10, 2))

from datetime import datetime, timedelta
import sqlite3

COUNT_DAYS = 366
COUNT_EMPLOYEES_PER_DAY = 10
COUNT_EMPLOYEES = 366
COUNT_WORKING_DAYS_FOR_EVERYONE_EMPLOYEE = COUNT_DAYS * COUNT_EMPLOYEES_PER_DAY // COUNT_EMPLOYEES
WEEK_DAYS = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
SECTIONS = ['футбол', "хоккей", "шахматы", "SUP сёрфинг", "бокс", "Dota2", "шах-бокс"]

sql_request_drop_all_rows = """
    DELETE FROM table_friendship_schedule
"""

sql_request_get_all_employees = """
    SELECT id, preferable_sport FROM table_friendship_employees
"""

sql_request_insert_employee = """
    INSERT INTO table_friendship_schedule (employee_id, date)
        VALUES (?,?)
"""


with sqlite3.connect("../homework.db") as conn:
    cursor = conn.cursor()
    cursor.execute(sql_request_drop_all_rows)
    employees = cursor.execute(sql_request_get_all_employees).fetchall()
    working_days = {employee[0]: 0 for employee in employees}
    today = datetime.strptime("2020-01-01", "%Y-%m-%d")
    workers_on_day = {today + timedelta(days=i): 0 for i in range(366)}
    for day, employee in workers_on_day.items():
        for id, sport in employees:
            if WEEK_DAYS[day.weekday()] == WEEK_DAYS[SECTIONS.index(sport)]:
                continue
            if working_days[id] != COUNT_WORKING_DAYS_FOR_EVERYONE_EMPLOYEE + 1:
                cursor.execute(sql_request_insert_employee, (id, str(day)[:10]))
                working_days[id] += 1
                workers_on_day[day] += 1
                if workers_on_day[day] == 10:
                    break
import sqlite3

sql_request_salary_worker = """SELECT salary FROM 'table_effective_manager' WHERE name = ?
"""
sql_request_update_salary = """UPDATE 'table_effective_manager' SET salary = ? WHERE name = ?
"""
sql_request_delete_worker = """DELETE FROM 'table_effective_manager' WHERE name = ?
"""
def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
          name: str,
) -> None:
    cursor.execute(sql_request_salary_worker, (name, ))
    salary = cursor.fetchone()[0]
    print("Зарплата сотрудника составляет:", salary)
    new_slary = salary / 100 * 10 + salary
    if new_slary > salary_ivan_sovin:
        cursor.execute(sql_request_delete_worker, (name, ))
        print(f"Зарплата оказалась высокой и сотрудник {name} был уволен")
    else:
        cursor.execute(sql_request_update_salary, (new_slary, name))
        print(f"Зарплата сотрудника {name} была повышена и сейчас составляет {new_slary}")

if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor = conn.cursor()
        name = input("ВВедите имя сотрудника:\n")
        cursor.execute(sql_request_salary_worker, ("Иван Совин", ))
        salary_ivan_sovin = cursor.fetchone()[0]
        print("Зарплата Ивана Совина: ", salary_ivan_sovin)
        ivan_sovin_the_most_effective(cursor, name)
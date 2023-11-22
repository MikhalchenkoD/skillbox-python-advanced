import sqlite3
import random

football_commands = "Ювентус Турин  Барселона Барселона  РеалМадрид Мадрид  " \
                    "МанчестерЮнайтед Манчестер  Челси Лондон  Арсенал Лондон  ЦСКА Москва " \
                    " Ливерпуль Ливерпуль  Зенит Санкт-Петербург  Спартак Москва  Милан Милан  Бавария Мюнхен" \
                    "  БоруссияД Дортмунд  Локомотив Москва  Интер Милан  Анжи Махачкала  Рома Рим  " \
                    "Валенсия Валенсия  МанчестерСити Англия".split("  ")

football_rating = "1 2 3".split(" ")

sql_request_for_table_uefa_commands = """INSERT INTO 'uefa_commands' 
(command_number, command_name, command_country, command_level) VALUES (?, ?, ?, ?)
"""
sql_request_for_table_uefa_draw = """INSERT INTO 'uefa_draw' (command_number, group_number) VALUES (?, ?)
"""
def generate_test_data(
        cursor: sqlite3.Cursor,
        number_of_groups: int
) -> None:
    lst_tuples_sql_request = []
    lst_comm_level = [number_of_groups, number_of_groups*2, number_of_groups]
    lst_comm_level_group = [[1, 2, 1] for x in range(number_of_groups)]
    lst_tuples_sql_request_2 = []
    for i in range(1, number_of_groups * 4 + 1):
        choice = random.choice(football_commands).split(" ")
        random_level = int(random.choice(football_rating))
        while lst_comm_level[random_level-1] == 0:
            random_level = int(random.choice(football_rating))

        k = random_level - 1
        count = 0
        while lst_comm_level_group[count][k] == 0:
            count += 1
        else:
            lst_comm_level_group[count][k] -= 1
            lst_tuples_sql_request_2.append((i, count+1))
        lst_comm_level[random_level-1] -= 1
        lst_tuples_sql_request.append((i, choice[0], choice[1], random_level))
    cursor.executemany(sql_request_for_table_uefa_commands, lst_tuples_sql_request)
    cursor.executemany(sql_request_for_table_uefa_draw, lst_tuples_sql_request_2)





if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor = conn.cursor()
        number_commands = int(input("Введите количество групп:\n"))
        generate_test_data(cursor, number_commands)
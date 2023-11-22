import sqlite3
from typing import Any, Optional, List

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]


class Book:

    def __init__(self, id: Optional[int], title: str, author: str, count: int = 0) -> None:
        self.id: Optional[int] = id
        self.title: str = title
        self.author: str = author
        self.count: int = count

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_books` (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT, 
                    author TEXT,
                    count INTEGER default 0
                )
                """
            )
            cursor.executemany(
                """
                INSERT INTO `table_books`
                (title, author) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_records
                ]
            )


def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books`
            """
        )
        return [Book(*row) for row in cursor.fetchall()]

def add_book(book: Book) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        query = f"""
                INSERT INTO table_books (title, author) VALUES 
                (?, ?)
                    """
        cursor.execute(query, (book.title, book.author))


def get_books(author: str) -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * from `table_books` WHERE author = '{author}'
            """
        )
        return [Book(*row) for row in cursor.fetchall()]

def get_book_by_id(id :int) -> Book:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT * from `table_books` WHERE id = {id}
            """
        )
        return Book(*cursor.fetchone())


def update_count_many_books(books: List[Book]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        parameters = []
        query = """
            UPDATE table_books SET count= :count
                WHERE id= :id
        """
        for book in books:
            parameters.append({
                "id": book.id,
                "count": book.count + 1
            })
        cursor.executemany(query, parameters)

def update_count_book(book: Book) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        query = """
            UPDATE table_books SET count= :count
                WHERE id= :id
        """
        cursor.execute(query, {"id": book.id, "count": book.count + 1})
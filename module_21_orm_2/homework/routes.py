from datetime import datetime, timedelta
from flask import jsonify, Flask, request
from sqlalchemy import create_engine, func, extract, desc
from sqlalchemy.orm import sessionmaker, selectinload
from models import Base, Books, Authors, Students, ReceivingBooks
from python_advanced.module_20_orm_1.homework.app import initialize_db

engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)


# Получение всех книг
@app.route('/books', methods=['GET'])
def get_all_books():
    books = session.query(Books).options(selectinload(Books.author)).all()
    book_list = [{"id": book.id, "name": book.name, "release_date": book.release_date, "author": {
        "id": book.author.id, "name": book.author.name, "surname": book.author.surname}} for book in books]
    session.close()
    return jsonify(book_list)


# Получение количества оставшихся в библиотеке книг по автору
@app.route('/books/count_by_author/<int:author_id>', methods=['GET'])
def get_book_count_by_author(author_id):
    book_count = session.query(func.sum(Books.count)).filter(Books.author_id == author_id).scalar()
    session.close()
    return jsonify({"count": book_count})


# Получение списка книг, которые студент не читал, но уже брал другие книги этого автора
@app.route('/books/unread_by_student/<int:student_id>', methods=['GET'])
def get_unread_books_by_student(student_id):
    student = session.query(Students).get(student_id)
    if not student:
        return jsonify({"error": "Студент не найден"})

    books_by_author = session.query(Books).filter(Books.author_id.in_(
        [book.author_id for book in student.books if book.date_of_return]
    )).all()

    book_list = [{"id": book.id, "name": book.name, "release_date": book.release_date} for book in books_by_author]
    session.close()
    return jsonify(book_list)


# Получение среднего количества книг, которые студенты брали в этом месяце
@app.route('/students/average_books_per_month', methods=['GET'])
def get_average_books_per_month():
    current_month = datetime.now().month
    books_count = session.query(func.count(ReceivingBooks.id)).filter(
        extract('month', ReceivingBooks.date_of_issue) == current_month).scalar()
    student_count = session.query(func.count(Students.id)).scalar()

    average_books_per_month = books_count / student_count if student_count else 0
    session.close()
    return jsonify({"average_books_per_month": average_books_per_month})


# Получение самой популярной книги среди студентов с средним баллом больше 4.0
@app.route('/books/most_popular_among_high_achievers', methods=['GET'])
def get_most_popular_book_among_high_achievers():
    high_achievers = session.query(Students).filter(Students.average_score > 4.0).all()

    book_counts = {}
    for student in high_achievers:
        for book in student.books:
            book_counts[book.id] = book_counts.get(book.id, 0) + 1

    most_popular_book_id = max(book_counts, key=book_counts.get) if book_counts else None
    most_popular_book = session.query(Books).filter(Books.id == most_popular_book_id).first()
    session.close()

    return jsonify({"most_popular_book": {
        "id": most_popular_book.id,
        "name": most_popular_book.name,
        "release_date": most_popular_book.release_date
    }})


# Получение ТОП-10 самых читающих студентов в этом году
@app.route('/students/top_readers', methods=['GET'])
def get_top_readers():
    top_readers = session.query(Students).order_by(desc(Students.books_count)).limit(10).all()

    top_readers_list = [{"id": student.id, "name": student.name, "surname": student.surname,
                         "books_count": student.books_count} for student in top_readers]

    session.close()
    return jsonify(top_readers_list)


# Роут для массовой вставки студентов из CSV
@app.route('/students/bulk_insert', methods=['POST'])
def bulk_insert_students():
    if 'file' not in request.files:
        return jsonify({"error": "Отсутствует файл"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Файл не выбран"})

    if file and file.filename.endswith('.csv'):
        try:
            students_data = file.read().decode('utf-8').split('\n')
            students_data = [row.split(';') for row in students_data if row]
            students_dicts = []
            for row in students_data:
                student_dict = {
                    'name': row[0].strip(),
                    'surname': row[1].strip(),
                    'phone': row[2].strip(),
                    'email': row[3].strip(),
                    'average_score': float(row[4].strip()),
                    'scholarship': True if row[5].strip().lower() == 'true' else False
                }
                students_dicts.append(student_dict)

            session.bulk_insert_mappings(Students, students_dicts)
            session.commit()
            session.close()
            return jsonify({"message": "Студенты успешно добавлены"})
        except Exception as e:
            session.rollback()
            session.close()
            return jsonify({"error": "Произошла ошибка при добавлении студентов: {}".format(str(e))})
    else:
        return jsonify({"error": "Недопустимый тип файла"})


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    initialize_db()
    app.run(debug=True)

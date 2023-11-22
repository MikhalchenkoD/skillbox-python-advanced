from flask import Flask, render_template
from typing import List
from flask import request, Response
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

from models import init_db, get_all_books, DATA, Book, add_book, get_books, get_book_by_id, update_count_book, \
    update_count_many_books

app: Flask = Flask(__name__)


def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books() -> str:
    books = get_all_books()
    update_count_many_books(books)
    return render_template(
        'index.html',
        books=books,
    )


class AddBookForm(FlaskForm):
    book_title = StringField(validators=[InputRequired()])
    author_name = StringField(validators=[InputRequired()])


@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form() -> str | Response:
    if request.method == 'GET':
        return render_template('add_book.html')
    elif request.method == "POST":
        form = AddBookForm(request.form)
        if form.validate_on_submit():
            book = Book(
                title=request.form["book_title"],
                author=request.form["author_name"],
                id=None
            )
            add_book(book)
            return Response({"msg": "Ok"}, status=200, mimetype='application/json')
        else:
            return Response(status=418)

@app.route('/books/author', methods=['GET', 'POST'])
def get_books_for_author() -> Response:
    if request.method == "GET":
        return render_template("get_author.html")
    elif request.method == "POST":
        if "author" in request.form:
            books = get_books(request.form["author"])
            update_count_many_books(books)
            return render_template(
                'index.html',
                books=books,
            )
        else:
            return Response(status=418)


@app.route('/books/<id>', methods=['GET'])
def get_book(id: int) -> str | Response:
    book = get_book_by_id(id)
    print(book)
    if book:
        update_count_book(book)
        return render_template("details.html", book=book)
    else:
        return Response(status=418)

if __name__ == '__main__':
    init_db(DATA)
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
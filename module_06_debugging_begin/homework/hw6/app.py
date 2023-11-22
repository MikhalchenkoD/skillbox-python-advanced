"""
Заменим сообщение "The requested URL was not found on the server" на что-то более информативное.
Например, выведем список всех доступных страниц с возможностью перехода по ним.

Создайте Flask Error Handler, который при отсутствии запрашиваемой страницы будет выводить
список всех доступных страниц на сайте с возможностью перехода на них.
"""

from flask import Flask, url_for

app = Flask(__name__)


@app.route('/dogs')
def dogs():
    return 'Страница с пёсиками'


@app.route('/cats')
def cats():
    return 'Страница с котиками'


@app.route('/cats/<int:cat_id>')
def cat_page(cat_id: int):
    return f'Страница с котиком {cat_id}'


@app.route('/index')
def index():
    return 'Главная страница'


@app.errorhandler(404)
def handle_exception(e: 404):
    lst = []
    for rule in app.url_map.iter_rules():
        url = "http://localhost:5000" + str(rule.rule)
        lst.append(f"<a href='{url}'>{url}</a>")
    return f"Данная страница не найдена. Вы можете перейти по следующим ссылкам:<br>" \
           f"{'<br>'.join(lst[1:])}", 404


if __name__ == '__main__':
    app.run(debug=True)

"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""

from flask import Flask
from datetime import datetime

app = Flask(__name__)

weekday = datetime.today().weekday()
days = ('понедельника', 'вторника', 'среды', 'четверга', 'пятницы', 'субботы', 'воскресенья')


@app.route('/hello-world/...')
def hello_world(name):
    if weekday == 0 or weekday == 1 or weekday == 3 or weekday == 6:
        return f"Привет, {name}! Хорошего {days[weekday]}"
    else:
        return f"Привет, {name}! Хорошей {days[weekday]}"


if __name__ == '__main__':
    app.run(debug=True)

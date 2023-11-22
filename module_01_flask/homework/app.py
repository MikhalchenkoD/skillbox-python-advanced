import datetime
from flask import Flask
import random
import datetime
import os
import re

app = Flask(__name__)

cars = 'Chevrolet, Renault, Ford, Lada'


@app.route('/hello_world')
def hello():
    return 'hello word'


@app.route('/cars')
def carss():
    global cars
    return cars


@app.route('/cats')
def cats():
    cats_list = ['корниш-рекс', 'русская голубая', 'шотландская вислоухая', 'мейн-кун', 'манчкин']
    random_int = round(random.randrange(len(cats_list)))
    return cats_list[random_int]


@app.route('/get_time/now')
def get_time_now():
    return 'Точное время: {current_time}'.format(current_time=datetime.datetime.now())


@app.route('/get_time/future')
def get_time():
    time_after_hour = datetime.datetime.now() + datetime.timedelta(hours=1)
    return f"Точное время через час будет {time_after_hour}"

base_dir = os.path.dirname(os.path.abspath(__file__))
book_file = os.path.join(base_dir, 'war_and_peace.txt')

with open(book_file, 'r', encoding='utf-8') as file:
    fille = file.read()
words = fille.split()

lst = []
for iword in words:
    word = re.search(r'\b[а-яА-Я]+\b', iword)
    if word:
        lst.append(word.group())


@app.route('/get_random_word')
def get_random_word():
    global lst
    return random.choice(lst)


@app.route('/counter')
def counter():
    global counter_visit
    counter_visit += 1
    return str(counter_visit)


if __name__ == '__main__':
    app.run(debug=True)

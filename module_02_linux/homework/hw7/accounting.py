"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""

from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int):
    day = int(date[6:8])
    month = int(date[4:6])
    year = int(date[:4])
    global storage
    storage.setdefault(year, {}).setdefault(month, {}).setdefault(day, 0)
    storage[year][month][day] += number
    return f"Дата: {year}-{month}-{day} <br>Траты: {str(storage[year][month][day])}"


@app.route("/calculate/<int:year>")
def calculate_year(year: int):
    global storage
    summ = 0
    for value in storage[year].values():
        summ += sum(value.values())
    return f"Траты за год({year}): {str(summ)}"


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int):
    global storage
    return f"Траты за месяц({year}-{month}): {str(sum(storage[year][month].values()))}"


if __name__ == "__main__":
    app.run(debug=True)

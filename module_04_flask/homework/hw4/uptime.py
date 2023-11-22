"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""
import sys

from flask import Flask

app = Flask(__name__)

line = sys.stdin.readline()
args = line.split(' ')
res_line = args[1:]
res_line = ''.join(res_line)


@app.route("/uptime", methods=['GET'])
def uptime() -> str:
    UPTIME = res_line
    return f"Current uptime is {UPTIME}"


if __name__ == '__main__':
    app.run(debug=True)

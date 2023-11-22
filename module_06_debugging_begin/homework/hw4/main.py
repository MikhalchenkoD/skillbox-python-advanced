"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
import itertools
import json
import subprocess
from collections import Counter
from subprocess import CompletedProcess
from typing import Dict, Any

with open("skillbox_json_messages.log", "r") as file:
    logs = [json.loads(line) for line in file.readlines()]


def task1() -> dict[str, str]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    lst_levels_logs = ["DEBUG", "INFO", "WARNING", "ERROR"]
    lvl_dict = dict()
    for level_log in lst_levels_logs:
        logs = subprocess.run(["grep", "-c", f'"level": "{level_log}"', "skillbox_json_messages.log"], capture_output=True, text=True)
        output = logs.stdout.strip()
        lvl_dict[level_log] = output
    return lvl_dict

def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """
    logs_by_hour = {}
    for hour, log_group in itertools.groupby(
            logs, key=lambda j: j["time"].split(":")[0]
    ):
        logs_by_hour[hour] = len(list(log_group))
    return max(logs_by_hour, key=logs_by_hour.get)


def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    command = ["grep", "-c", 'time": "03:1[8-9]:[0-5][0-9]", "level": "INFO"', "skillbox_json_messages.log"]
    result = subprocess.run(command, capture_output=True, text=True)
    output = int(result.stdout.strip())
    return output


def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    command = ["grep", "-c", '\w*\\b[пП]ароль\\b\w*', "skillbox_json_messages.log"]
    result = subprocess.run(command, capture_output=True, text=True)
    output = int(result.stdout.strip())
    return output


def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    warnings = [log["message"] for log in logs if log["level"] == "WARNING"]
    words = [word for word in (warning.split() for warning in warnings)]

    most_frequent, count = Counter(
        [item for sublist in words for item in sublist]
    ).most_common(1)[0]

    return f"Самое частое слово: {most_frequent}, кол-во раз: {count}"


if __name__ == '__main__':
    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')

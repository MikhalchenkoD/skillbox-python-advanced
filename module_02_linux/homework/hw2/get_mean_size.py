"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys
from typing import List

lines = sys.stdin.readlines()[1:]


def get_mean_size(ls_output: List):
    size = 0
    count = 0
    for i_line in ls_output:
        count += 1
        size += int(i_line.split()[4])
    return size / count


if __name__ == '__main__':
    mean_size: float = get_mean_size(lines)
    print(mean_size)

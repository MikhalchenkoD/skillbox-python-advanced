"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""
import os.path


def get_summary_rss(ps_output_file_path: str):
    summ = 0
    with open(ps_output_file_path, 'r') as output_file:
        lines = output_file.readlines()[1:]
        for i_line in lines:
            summ += int(i_line.split()[5])
    bits = summ
    kbits = summ / 1024
    mbits = kbits / 1024
    return f"Объем потребляемой памяти: {bits} B, {round(kbits, 2)} KiB, {round(mbits, 2)} MiB"


if __name__ == '__main__':
    path: str = os.path.abspath('output_file.txt')
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)

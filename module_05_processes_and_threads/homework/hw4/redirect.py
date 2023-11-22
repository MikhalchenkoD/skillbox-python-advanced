"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""
import sys


class Redirect:
    def __init__(self, stdout=None, stderr=None):
        self.stdout = stdout
        self.stderr = stderr
        self.stdout_orig = None
        self.stderr_orig = None

    def __enter__(self):
        if self.stdout is not None:
            self.stdout_orig = sys.stdout
            sys.stdout = self.stdout
        if self.stderr is not None:
            self.stderr_orig = sys.stderr
            sys.stderr = self.stderr

    def __exit__(self, exc_type, exc_value, traceback):
        if self.stdout is not None:
            sys.stdout = self.stdout_orig
        if self.stderr is not None:
            sys.stderr = self.stderr_orig
        if exc_type is not None and exc_value is not None:
            raise exc_value


if __name__ == '__main__':
    print('Hello stdout')
    stdout_file = open('stdout.txt', 'w')
    stderr_file = open('stderr.txt', 'w')

    try:
        with Redirect(stdout=stdout_file, stderr=stderr_file):
            print('Hello stdout.txt')
            raise Exception('Hello stderr.txt')
    except Exception as e:
        print(e)

    print('Hello stdout again')
    raise Exception('Hello stderr')



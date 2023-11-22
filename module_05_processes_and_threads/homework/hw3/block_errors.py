"""
Реализуйте контекстный менеджер, который будет игнорировать переданные типы исключений, возникающие внутри блока with.
Если выкидывается неожидаемый тип исключения, то он прокидывается выше.
"""

from typing import Collection, Type, Literal
from types import TracebackType


class BlockErrors:
    def __init__(self, errors: Collection) -> None:
        self.errors = errors

    def __enter__(self) -> Collection:
        return self.errors

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        for err in self.errors:
            if (err == exc_type) or (err == Exception) or (err == BaseException):
                return True


err_types = {BaseException}
with BlockErrors(err_types):
    a = 1 / '0'
print('Выполнено без ошибок')

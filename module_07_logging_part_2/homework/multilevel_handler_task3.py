import logging

class MultiLevelHandler(logging.Handler):
    def __init__(self, mode='a'):
        super().__init__()
        self.mode = mode
    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        with open(f"./calc_{record.levelname.lower()}.log", mode=self.mode) as f:
            f.write(message + "\n")

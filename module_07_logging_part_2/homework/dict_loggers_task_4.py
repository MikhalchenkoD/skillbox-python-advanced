import logging.handlers
import sys

from multilevel_handler_task3 import MultiLevelHandler

class ASCII(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return str.isascii(record.msg)

dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
           "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s"
        }
    },
    "filters": {
        "isascii": {
            "()": ASCII
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "stream": "sys.stdout",
            "filters": ["isascii"]
        },
        "multilevelfile": {
            "()": MultiLevelHandler,
            "level": "DEBUG",
            "formatter": "base",
            "filters": ["isascii"]
        },
        "time_rotating": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "base",
            "when": "h",
            "interval": 10,
            "backupCount": 1,
            "filename": "utils.txt",
            "filters": ["isascii"]
        },
        'server_handler': {
            '()': logging.handlers.HTTPHandler,
            'host': 'localhost:5000',
            'url': '/logs',
            'method': 'POST'
        }
    },
    "loggers": {
        "api": {
            "level": "DEBUG",
            "handlers": ["multilevelfile"],
            # "propagate": False
        },
        "utils": {
            "level": "INFO",
            "handlers": ["time_rotating"]
        },
        'server_log': {
            'level': 'DEBUG',
            'handlers': ['server_handler']
        }
    }
}

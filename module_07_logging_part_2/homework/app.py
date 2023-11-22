import sys
import logging.config
from utils import string_to_operator
# from multilevel_handler_task3 import MultiLevelHandler
from dict_loggers_task_4 import dict_config
from logging_tree import printout

logging.config.dictConfig(dict_config)

logger = logging.getLogger("api")


def calc(args):
    logger.debug(f"Arguments: {args}")
    num_1 = args[0]
    operator = args[1]
    num_2 = args[2]

    try:
        num_1 = float(num_1)
    except ValueError as e:
        logger.error('Error while converting number 1')
        logger.error(e)

    try:
        num_2 = float(num_2)
    except ValueError as e:
        logger.error('Error while converting number 1')
        logger.error(e)

    operator_func = string_to_operator(operator)

    result = operator_func(num_1, num_2)

    logger.debug(f"Result: {result}")
    logger.debug(f"{num_1} {operator} {num_2} = {result}")


if __name__ == '__main__':
    calc(sys.argv[1:])

import logging
from flask import Flask, request
from dict_loggers_task_4 import dict_config
from logging import config

app = Flask(__name__)


logger = logging.getLogger('server_log')
logging.config.dictConfig(dict_config)


@app.route('/logs/')
def get_logs():
    with open('utils.txt', 'r') as log_file:
        logs = log_file.read()
        logs = logs.replace('\n', '</br>')
    return logs


@app.route('/logs/', methods=['POST'])
def post_log():
    log_data = request.json
    print(log_data)
    if log_data is None:
        return 'Пустое тело запроса.', 400
    service_name = log_data.pop('server')
    print(service_name)

    try:
        level_str = log_data['level']
        print(level_str)
        level_num = getattr(logging, level_str.upper())
        print(level_num)

        print(logger.log(level_num, '{}: {}'.format(service_name, log_data['message']), extra=log_data))

        return 'Успех!'

    except (ValueError, KeyError) as err:
        logger.error('Ошибка лога: {}'.format(err))
        return 'Ошибка: {}'.format(err), 400


if __name__ == '__main__':
    app.run(debug=True)
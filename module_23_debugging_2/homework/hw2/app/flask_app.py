import time
import random

from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route('/one')
@metrics.counter('Counter', 'Counter for endpoint')
def first_route():
    return 'ok'


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)

import time

from flask import Flask, jsonify

application = Flask(__name__)


@application.route('/long_task')
def long_task():
   time.sleep(300)
   return jsonify(message='We did it!')
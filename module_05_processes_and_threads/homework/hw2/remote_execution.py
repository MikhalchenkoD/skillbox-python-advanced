"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""

from flask import Flask
import subprocess
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange

app = Flask(__name__)

class RunCodeForm(FlaskForm):
    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(validators=[NumberRange(min=1, max=30)])

@app.route('/runcode', methods=["POST"])
def run_code():
    form = RunCodeForm()

    if form.validate_on_submit():
        code, timeout = form.code.data, form.timeout.data

        r = subprocess.Popen(["prlimit", "--nproc=1:1", "python", "-c", code],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            output, errors = r.communicate(timeout=timeout)
            if errors:
                return errors
            return output
        except Exception:
            r.kill()
            raise ValueError("Timeout reached")

    return f"Invalid input: {form.errors}", 400


if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run()
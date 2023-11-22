FROM test_app

RUN mkdir /api

COPY requirements.txt /app/

RUN python -m pip install -r /api/requirements.txt

COPY app.py /app/

WORKDIR /app

ENTRYPOINT ["python", "app.py"]
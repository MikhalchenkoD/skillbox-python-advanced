FROM python:3.8

RUN pip install Flask gunicorn psycopg2-binary requests sqlalchemy alembic

COPY /flask /app
WORKDIR /app

CMD ["gunicorn", "-b", "0.0.0.0:8000", "routes:app"]

FROM python:3.8

RUN pip install poetry==1.1.12

COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml

WORKDIR /app

RUN poetry install

COPY . /app

CMD poetry run uvicorn main:app --host 0.0.0.0 --port 8085 --workers 12
FROM python:3.7.5-alpine

WORKDIR /code

ENV FLASK_APP webapi
ENV FLASK_RUN_HOST 0.0.0.0

RUN pip install pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system --dev

COPY . .

RUN flask init-db --datafile tests/data.sql
CMD ["flask", "run"]

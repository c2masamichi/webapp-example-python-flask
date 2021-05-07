FROM python:3.9.5-slim-buster

WORKDIR /code

ENV FLASK_APP webapi
ENV FLASK_RUN_HOST 0.0.0.0

RUN pip install pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system --dev

COPY . .

CMD ["flask", "run"]

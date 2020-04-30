FROM python:3.8.2-alpine

WORKDIR /code

ENV FLASK_APP cms
ENV FLASK_RUN_HOST 0.0.0.0

RUN pip install pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system --dev

COPY . .

CMD ["flask", "run"]

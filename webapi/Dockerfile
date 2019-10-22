FROM python:3.7.4

WORKDIR /code

RUN pip install pipenv
COPY Pipfile ./
COPY Pipfile.lock ./
RUN pipenv install --system

COPY . .

ENV FLASK_APP webapi
ENV FLASK_RUN_HOST 0.0.0.0

CMD ["flask", "run"]

FROM python:3.7.4

WORKDIR /code

ENV FLASK_APP webapi
ENV FLASK_RUN_HOST 0.0.0.0

RUN pip install pipenv
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system

COPY . .

CMD ["flask", "run"]

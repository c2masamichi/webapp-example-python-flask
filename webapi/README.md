# Docker

## DB Setup

```
$ docker-compose up -d db
$ docker-compose run web flask init-db
Initialized the database.
```

Init DB wth test data

```
$ docker-compose run web flask init-db --withdata
Initialized the database.
```

## Run

```
docker-compose up web
```

## Test

```
docker-compose run web pytest
```

# Docker

## Devepolment

### DB Setup

```
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml -p webapi_dev up -d db
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml -p webapi_dev run web flask init-db
Initialized the database.
```

Init DB wth test data

```
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml -p webapi_dev run web flask init-db --withdata
Initialized the database.
```

### Run App

```
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml -p webapi_dev up web
```

### Clear

```
$ docker-compose -p webapi_dev down
```

## Testing

### Run Test

```
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml -p webapi_test run web pytest
```

### Clear

```
$ docker-compose -p webapi_test down
```

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

### DB Setup

```
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml -p webapi_test up -d db
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml -p webapi_test run web flask init-db
Initialized the database.
```

### Run Test

```
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml -p webapi_test run web pytest
```

Run with coverage report

```
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml -p webapi_test run web coverage run -m pytest
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml -p webapi_test run web coverage report
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml -p webapi_test run web coverage html 
```

### Clear

```
$ docker-compose -p webapi_test down
```

# Docker

## Devepolment

### Build

```
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml -p flask_webapi_dev build
```

### Run App

```
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml -p flask_webapi_dev up -d
$ docker exec -it flask_webapi_dev_app_1 flask init-db
```

load test data

```
$ docker exec -it flask_webapi_dev_app_1 flask load-data
```

### Clear

```
$ docker-compose -p flask_webapi_dev down
```

## Testing

### Build

```
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml -p flask_webapi_test build
```

### Run Test

```
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml -p flask_webapi_test up -d
$ docker exec -it flask_webapi_test_app_1 pytest
```

Run with coverage report

```
$ docker exec -it flask_ebapi_test_app_1 coverage run -m pytest
$ docker exec -it flask_webapi_test_app_1 coverage report
$ docker exec -it flask_webapi_test_app_1 coverage html
```

### Clear

```
$ docker-compose -p flask_webapi_test down
```

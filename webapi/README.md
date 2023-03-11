# Docker

## Devepolment

### Build

```
$ docker-compose -p flask_webapi build
```

### Run App

```
$ docker-compose -p flask_webapi up -d
$ docker exec -it flask_webapi_app_1 flask init-db
```

load test data

```
$ docker exec -it flask_webapi_app_1 flask load-data
```

http://localhost:15000/api/v1/products

### Run Test

```
$ docker-compose -p flask_webapi up -d
$ cd app/
$ docker exec -it flask_webapi_app_1 pytest
```

Run with coverage report

```
$ docker exec -it flask_webapi_app_1 coverage run -m pytest
$ docker exec -it flask_webapi_app_1 coverage report
$ docker exec -it flask_webapi_app_1 coverage html
```

### Clear

```
$ docker-compose -p flask_webapi down
```

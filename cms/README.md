# Docker

## Devepolment

### Build

```
$ docker-compose -p flask_cms build
```

### Run App

```
$ docker-compose -p flask_cms up -d
$ docker exec -it flask_cms_app_1 flask init-db
```

load test data

```
$ docker exec -it flask_cms_app_1 flask load-data
```

create superuser

```
$ docker exec -it flask_cms_app_1 flask create-superuser --username dev-user
```

### Run Test

```
$ docker-compose -p flask_cms up -d
$ cd app/
$ docker exec -it flask_cms_app_1 pytest
```

Run with coverage report

```
$ docker exec -it flask_cms_app_1 coverage run -m pytest
$ docker exec -it flask_cms_app_1 coverage report
$ docker exec -it flask_cms_app_1 coverage html
```

### Clear

```
$ docker-compose -p flask_cms down
```

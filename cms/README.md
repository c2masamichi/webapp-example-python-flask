# Docker

## Devepolment

### Build

```
$ docker-compose build
```

### Run App

```
$ docker-compose up -d
$ docker exec -it cms_app_1 flask init-db
```

load test data

```
$ docker exec -it cms_app_1 flask load-data
```

create superuser

```
$ docker exec -it cms_app_1 flask create-superuser --username dev-user
```

### Run Test

```
$ docker-compose up -d
$ cd app/
$ docker exec -it cms_app_1 pytest
```

Run with coverage report

```
$ docker exec -it cms_app_1 coverage run -m pytest
$ docker exec -it cms_app_1 coverage report
$ docker exec -it cms_app_1 coverage html
```

### Clear

```
$ docker-compose down
```

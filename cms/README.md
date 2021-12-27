# Docker

## Devepolment

### Build

```
docker-compose -f docker-compose.yml -f docker-compose.dev.yml -p flask_cms_dev build
```

### Run App

```
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml -p flask_cms_dev up -d
$ docker exec -it flask_cms_dev_app_1 flask init-db
```

load test data

```
$ docker exec -it flask_cms_dev_app_1 flask load-data
```

create superuser

```
$ docker exec -it flask_cms_dev_app_1 flask create-superuser --username dev-user
```

### Clear

```
$ docker-compose -p flask_cms_dev down
```

## Testing

### Build

```
docker-compose -f docker-compose.yml -f docker-compose.test.yml -p flask_cms_test build
```

### Run Test

```
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml -p flask_cms_test up -d
$ docker exec -it flask_cms_test_app_1 pytest
```

Run with coverage report

```
$ docker exec -it flask_cms_test_app_1 coverage run -m pytest
$ docker exec -it flask_cms_test_app_1 coverage report
$ docker exec -it flask_cms_test_app_1 coverage html
```

### Clear

```
$ docker-compose -p flask_cms_test down
```

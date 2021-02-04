# Docker

## Devepolment

### Run App

```
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml -p flask_cms_dev up -d
$ docker exec -it flask_cms_dev_web_1 flask init-db
```

Init DB wth test data

```
$ docker exec -it flask_cms_dev_web_1 flask init-db --withdata
```

create superuser

```
$ docker exec -it flask_cms_dev_web_1 flask create-superuser --username dev-user
```

### Clear

```
$ docker-compose -p flask_cms_dev down
```

## Testing

### Run Test

```
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml -p flask_cms_test up -d
$ docker exec -it flask_cms_test_web_1 pytest
```

Run with coverage report

```
$ docker exec -it flask_cms_test_web_1 coverage run -m pytest
$ docker exec -it flask_cms_test_web_1 coverage report
$ docker exec -it flask_cms_test_web_1 coverage html
```

### Clear

```
$ docker-compose -p flask_cms_test down
```

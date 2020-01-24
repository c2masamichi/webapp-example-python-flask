# Docker

## Devepolment

### DB Setup

```
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml -p cms_dev up -d db
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml -p cms_dev run web flask init-db
Initialized the database.
```

Init DB wth test data

```
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml -p cms_dev run web flask init-db --withdata
Initialized the database.
```

### Run App

```
$ docker-compose -f docker-compose.yml -f docker-compose.dev.yml -p cms_dev up web
```

### Clear

```
$ docker-compose -p cms_dev down
```

## Testing

### DB Setup

```
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml -p cms_test up -d db
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml -p cms_test run web flask init-db
Initialized the database.
```

### Run Test

```
$ docker-compose -f docker-compose.yml -f docker-compose.test.yml -p cms_test run web pytest
```

### Clear

```
$ docker-compose -p cms_test down
```

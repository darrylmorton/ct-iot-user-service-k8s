# ct-iot-user-service

## Description
The `user-service` is responsible for managing users of the `ct-iot` platform.

[Diagrams](./docs/DIAGRAMS.md)

## Requirements
Python 3.11.9  
Poetry 1.7.1

## Install
```
poetry install
```

## Environment Variables
```
AWS_REGION=
SENTRY_ENVIRONMENT=
SENTRY_DSN=
SENTRY_TRACES_SAMPLE_RATE=
SENTRY_PROFILES_SAMPLE_RATE=
SENTRY_SAMPLE_RATE=

SERVICE_NAME=
LOG_LEVEL=
ENVIRONMENT=

AUTH_SERVICE_URL=

DB_HOST=
DB_PORT=
DB_USERNAME=
DB_PASSWORD=
DB_NAME=
```

## Run
Refer to [ct-iot-authentication-service repository README.md](https://github.com/darrylmorton/ct-iot-authentication-service/blob/main/README.md) for building the required dependency docker image.

### Development
```
docker compose -f docker-compose-local.yml up
make dev-server-start
```
Swagger docs: http://localhost:8001/docs

### Test
```
docker compose -f docker-compose-local.yml up
make test
```

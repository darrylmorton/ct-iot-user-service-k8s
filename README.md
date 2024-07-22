# ct-iot-user-service

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
SENTRY_DSN=
SENTRY_TRACES_SAMPLE_RATE=
SENTRY_PROFILES_SAMPLE_RATE=
SENTRY_SAMPLE_RATE=

SERVICE_NAME=
LOG_LEVEL=
ENVIRONMENT=

AUTH_SERVICE_HOST=
AUTH_SERVICE_PORT=

DB_HOST=
DB_PORT=
DB_USERNAME=
DB_PASSWORD=
DB_NAME=
```

## Dev
Swagger docs: http://localhost:8002/docs
```
make dev-server-start
```

## Prod
```
make server-start
```

## Test
```
make test-unit
make test-integration
```

# ct-iot-user-service

## Requirements
Python 3.12.0
Poetry 1.7.1

## Install
```
poetry install
```

## Environment Variables
```
SERVICE_NAME
LOG_LEVEL
ENVIRONMENT
APP_PORT
DB_HOST=
DB_PORT=
DB_USERNAME=
DB_PASSWORD=
DB_NAME=
```

## Dev
Swagger docs: http://localhost:8001/docs
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

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
SERVICE_NAME="user-service"
LOG_LEVEL="DEBUG"
ENVIRONMENT="DEVELOPMENT"
```

## Dev
Swagger docs: http://localhost:8001/docs
```
make run-dev
```

## Prod
```
make run
```

## Test
```
make test
```

# ct-iot-user-service

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
```
poetry run uvicorn src.main:app --reload --port 8001
```

## Test
```
poetry run pytest
```

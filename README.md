# ct-iot-user-service-k8s

## Description
The `user-service` is responsible for managing users of the `ct-iot` platform.

[Diagrams](./docs/DIAGRAMS.md)

## Requirements
Python 3.11.9  
Poetry 1.7.1
Act 0.2.79+ (optional: for testing GitHub workflows locally)  
GitHub CLI 2.62.0+ (optional: for manually managing GitHub releases)

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
Refer to the `authentication-service` [repository](https://github.com/darrylmorton/ct-iot-authentication-service/blob/main/README.md#build) for building the required dependency docker image.

### Development
```
docker compose -f docker-compose-local.yml up
make dev-server-start
```
Swagger docs: http://localhost:8002/docs

### Test
```
docker compose -f docker-compose-local.yml up
make migrations
make test
```

#### GitHub Workflows
```
act --container-architecture linux/amd64 -W ./.github/workflows/tests.yml
```


### Helm | K8s 
```
helm plugin install https://github.com/jkroepke/helm-secrets --version v4.6.2
helm secrets encrypt helm/user-service/secrets-decrypted/credentials.yaml.dec > helm/user-service/secrets/credentials.yaml helm/user-service -n ct-iot

# development
helm secrets install user-service helm/user-service -f helm/user-service/local-values.yaml -f helm/user-service/secrets/credentials.yaml -n ct-iot
helm upgrade user-service helm/user-service -f helm/user-service/local-values.yaml -n ct-iot

k -n ct-iot port-forward svc/user-service 8002:9001 &

# production
helm secrets install user-service helm/user-service -f helm/user-service/values.yaml -f helm/user-service/secrets/credentials.yaml -n ct-iot
helm upgrade user-service helm/user-service -f helm/user-service/values.yaml -n ct-iot

helm uninstall user-service -n ct-iot
```

### Release
Automated via GitHub Actions. 

There's also a `GitHub Publish` workflow for performing a manual release which can be run with the following command:
```
gh release create {RELEASE_VERSION} --generate-notes
```
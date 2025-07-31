fmt:
	poetry run ruff format .
.PHONY:fmt

lint: fmt
	poetry run ruff check . --fix
.PHONY: lint

check-version: lint
	poetry run python scripts/check_version.py --latest-release-version $(RELEASE_VERSION)
.PHONY: check-version

local-build: lint
	DOCKER_BUILDKIT=1 docker build -t ct-iot-user-service:dev --target=runtime --progress=plain .
.PHONY: local-build

build: lint
	DOCKER_BUILDKIT=1 docker build -t ct-iot-user-service --platform=linux/amd64 --target=runtime --progress=plain .
.PHONY: build

dev-server-start: fmt
	poetry run uvicorn user_service.service:app --reload --port 8002
.PHONY: dev-server-start

server-start: fmt
	poetry run uvicorn user_service.service:app
.PHONY: server-start

migrations: fmt
	poetry run alembic upgrade head
.PHONY: migrations

migrations-rollback: fmt
	poetry run alembic downgrade -1
.PHONY: migrations-rollback

migrations-downgrade-base: fmt
	poetry run alembic downgrade base
.PHONY: migrations-downgrade-base

test-unit: fmt
	poetry run pytest tests/unit/
.PHONY: test-unit

test-integration: fmt
	poetry run pytest tests/integration/
.PHONY: test-integration

test: fmt
	poetry run pytest tests/
.PHONY: test

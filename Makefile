fmt:
	poetry run ruff format .
.PHONY:fmt

lint: fmt
	poetry run ruff check . --fix
.PHONY: lint

build: lint
	DOCKER_BUILDKIT=1 docker build --platform=linux/amd64 --target=runtime --progress=plain .
.PHONY: build

dev-server-start: fmt
	poetry run uvicorn --log-level=debug user_service.service:app --reload --port 8002
.PHONY: dev-server-start

server-start: fmt
	poetry run uvicorn user_service.service:app
.PHONY: server-start

run-migrations: fmt
	poetry run alembic upgrade head
.PHONY: run-migrations

run-migrations-rollback: fmt
	poetry run alembic downgrade -1
.PHONY: run-migrations-rollback

run-migrations-downgrade-base: fmt
	poetry run alembic downgrade base
.PHONY: run-migrations-downgrade-base

test-unit: fmt
	poetry run pytest tests/unit/
.PHONY: test-unit

test-integration: fmt
	poetry run pytest tests/integration/
.PHONY: test-integration

test: fmt
	poetry run pytest tests/
.PHONY: test

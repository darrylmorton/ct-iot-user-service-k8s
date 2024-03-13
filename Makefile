.DEFAULT_GOAL := build

fmt:
	poetry run ruff format .
.PHONY:fmt

lint: fmt
	poetry run ruff check . --fix
.PHONY:lint

run-dev: fmt
	poetry run uvicorn --log-level=debug src.user_service.service:server --reload --port 8001
.PHONY:run-dev

run: fmt
	poetry run uvicorn src.user_service.service:server --port 8001
.PHONY:run

run-migrations: fmt
	poetry run alembic upgrade head
.PHONY:run-migrations

run-migrations-rollback: fmt
	poetry run alembic downgrade -1
.PHONY:run-migrations-rollback

run-migrations-downgrade-base: fmt
	poetry run alembic downgrade base
.PHONY:run-migrations-downgrade-base

test-unit: fmt
	poetry run pytest tests/unit
.PHONY:test-unit

test-integration: fmt
	poetry run pytest tests/integration
.PHONY:test-integration

test-integration-with-server: fmt
	make -j 2 run test-integration
.PHONY:test-integration-with-server

test: fmt
	poetry run pytest tests
.PHONY:test
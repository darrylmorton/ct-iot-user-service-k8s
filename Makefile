.DEFAULT_GOAL := build

fmt:
	poetry run ruff format .
.PHONY:fmt

lint: fmt
	poetry run ruff check . --fix
.PHONY:lint

run-dev: fmt
	poetry run uvicorn --log-level=debug src.main:server --reload --port 8001
.PHONY:run-dev

run: fmt
	poetry run uvicorn src.main:server --port 8001
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

test: fmt
	poetry run pytest
.PHONY:test
.DEFAULT_GOAL := build

fmt:
	poetry run ruff format .
.PHONY:fmt

lint: fmt
	poetry run ruff check . --fix
.PHONY:lint

run-dev: fmt
	poetry run uvicorn src.main:server --reload --port 8001
.PHONY:run-dev

run: fmt
	poetry run uvicorn src.main:server --port 8001
.PHONY:run

test: fmt
	poetry run pytest
.PHONY:test
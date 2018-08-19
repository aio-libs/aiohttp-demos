export PYTHONPATH=.

PROJECT_NAME=graph

all: run

run:
	@python -m $(PROJECT_NAME)

mypy:
	@mypy $(PROJECT_NAME)

lint:
	@flake8 $(PROJECT_NAME)

test: lint
	@py.test

start_database:
	@docker-compose up -d postgres

start_redis:
	@docker-compose up -d redis

prepare_database:
	@python prepare_database.py

run_ui:
	@cd ui && yarn start

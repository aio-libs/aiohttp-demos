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
	@py.test --cov=graphql

start_database:
	@docker-compose up postgres -d


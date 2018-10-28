# Some simple testing tasks (sorry, UNIX only).

PROJECT_NAME=imagetagger

flake:
	flake8 $(PROJECT_NAME) setup.py

test:
	py.test -s -v  ./tests/

checkrst:
	python setup.py check --restructuredtext

cov cover coverage: flake checkrst
	py.test -s -v --cov-report term --cov-report html --cov $(PROJECT_NAME) ./tests
	@echo "open file://`pwd`/htmlcov/index.html"

clean:
	rm -rf `find . -name __pycache__`
	find . -type f -name '*.py[co]'  -delete
	find . -type f -name '*~'  -delete
	find . -type f -name '.*~'  -delete
	find . -type f -name '@*'  -delete
	find . -type f -name '#*#'  -delete
	find . -type f -name '*.orig'  -delete
	find . -type f -name '*.rej'  -delete
	rm -f .coverage
	rm -rf coverage
	rm -rf build
	rm -rf htmlcov
	rm -rf dist

run:
	python -m $(PROJECT_NAME)


.PHONY: flake clean

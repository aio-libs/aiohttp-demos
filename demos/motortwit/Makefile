# Some simple testing tasks (sorry, UNIX only).

FLAGS=


flake:
	flake8 motortwit setup.py

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f .coverage
	rm -rf coverage
	rm -rf build
	rm -rf htmlcov
	rm -rf dist

run:
	python -m motortwit

fake_data:
	python ./motortwit/generate_data.py

docker_start_mongo:
	docker-compose -f docker-compose.yml up -d mongo

docker_stop_mongo:
	docker-compose -f docker-compose.yml stop mongo

.PHONY: flake clean

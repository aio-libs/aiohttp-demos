# Some simple testing tasks (sorry, UNIX only).

FLAGS=


flake:
	flake8 shortify setup.py

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
	python -m shortify

docker_start_redis:
	docker-compose -f docker-compose.yml up -d redis

docker_stop_redis:
	docker-compose -f docker-compose.yml stop redis

.PHONY: flake clean

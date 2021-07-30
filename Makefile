clean:
	@rm -rf `find . -name __pycache__`
	@make -C docs clean

lint:
	@flake8 demos

test:
	@pytest -q demos/polls/tests
	@pytest -q demos/chat/tests
	@pytest -q demos/blog/tests
	@pytest -q demos/graphql-demo
	@SLACK_BOT_TOKEN=xxx GIPHY_API_KEY=xxx pytest -q demos/moderator_bot/tests

ci: lint test doc-spelling

doc:
	@make -C docs html SPHINXOPTS="-W -E"
	@echo "open file://`pwd`/docs/_build/html/index.html"

doc-spelling:
	@make -C docs spelling SPHINXOPTS="-W -E"

install:
	@pip install -U pip setuptools
	@pip install -Ur requirements-dev.txt
  	@pip install demos/polls
  	@pip install demos/chat
  	@pip install demos/blog
  	@pip install demos/graphql-demo
  	@pip install -r demos/moderator_bot/requirements-dev.txt

.PHONY: clean doc

clean:
	@rm -rf `find . -name __pycache__`
	@make -C docs clean

lint:
	@flake8 demos

test:
	@pytest demos/blog
	@pytest demos/chat
	@pytest demos/graphql-demo
	@pytest demos/imagetagger
	@pytest demos/moderator
	@SLACK_BOT_TOKEN=xxx GIPHY_API_KEY=xxx pytest demos/moderator_bot/tests
	@pytest demos/motortwit
	@pytest demos/polls
	@pytest demos/shortify

ci: lint test doc-spelling

doc:
	@make -C docs html SPHINXOPTS="-W -E"
	@echo "open file://`pwd`/docs/_build/html/index.html"

doc-spelling:
	@make -C docs spelling SPHINXOPTS="-W -E"

install:
	@pip install -U pip setuptools cython
	@pip install -r requirements-dev.txt
	@pip install -r demos/blog/requirements.txt
	@pip install -r demos/chat/requirements.txt
	@pip install -r demos/graphql-demo/requirements-dev.txt
	@pip install -r demos/imagetagger/requirements.txt
	@pip install -r demos/moderator/requirements-dev.txt
	@pip install -r demos/moderator_bot/requirements-dev.txt
	@pip install -r demos/motortwit/requirements.txt
	@pip install -r demos/polls/requirements-dev.txt
	@pip install -r demos/shortify/requirements.txt

.PHONY: clean doc

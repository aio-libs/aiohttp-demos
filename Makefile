clean:
	@rm -rf `find . -name __pycache__`
	@make -C docs clean

doc:
	@make -C docs html SPHINXOPTS="-W -E"
	@echo "open file://`pwd`/docs/_build/html/index.html"

doc-spelling:
	@make -C docs spelling SPHINXOPTS="-W -E"

install:
	@pip install -U pip setuptools
	@pip install -Ur requirements-dev.txt

.PHONY: clean doc

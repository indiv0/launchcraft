develop: setup-git
	@echo "--> Installing dependencies"
	pip install "setuptools>=0.9.8"
	pip install -e .
	pip install "file://`pwd`#egg=sentry[dev]"
	pip install "file://`pwd`#egg=sentry[tests]"
	@echo ""

setup-git:
	@echo "--> Installing git hooks"
	git config branch.autosetuprebase always
	cd .git/hooks && ln -sf ../../hooks/* ./
	@echo ""

clean:
	@echo "--> Cleaning pyc files"
	find . -name "*.pyc" -delete
	@echo "--> Cleaning directories"
	rm -rf logs/ build/ dist/
	@echo ""

test: develop lint test-python

test-python:
	@echo "--> Running Python tests"
	py.test tests || exit 1
	@echo ""

lint: lint-python

lint-python:
	@echo "--> Linting Python files"
	PYFLAKES_NODOCTEST=1 flake8 src/launchcraft tests
	@echo ""

coverage: develop
	coverage run --source=src/launchcraft -m py.test
	coverage html

publish:
	python setup.py sdist bdist_wheel upload

.PHONY: develop clean test test-python lint lint-python coverage publish

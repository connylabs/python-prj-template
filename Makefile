.PHONY: check clean-build clean-pyc clean-test help test prep-test test-all test-dep

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "test - run tests quickly with the default Python"
	@echo "prep-test - create the cookiecutter test app"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -rf cutterapp
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '.mypy_cache' -exec rm -fr {} +
	find . -name '.pyre' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

prep-test:
	rm -rf cutterapp
	cookiecutter --config-file tests/replay-config.yaml --no-input .

test-dep:
	pip install -r cutterapp/requirements.txt -U
	pip install -r cutterapp/requirements_dev.txt -U

test-all: prep-test test-dep test

test:
	make -C cutterapp test
	make -C cutterapp check

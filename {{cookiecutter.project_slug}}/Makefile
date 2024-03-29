.PHONY: black black-test check clean clean-build clean-pyc clean-test coverage dist dockerfile dockerfile-canary dockerfile-push docs flake8 gen-ci help install lint prepare pylint pylint-quick pyre release rename servedocs test test-all tox
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"
VERSION := `cat VERSION`
package := "{{ cookiecutter.package_name }}"

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc clean-test

clean-build:
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

lint:
	flake8 $(package) tests

test:
	py.test --cov=$(package) --cov-report=html --cov-report=term-missing  --verbose tests

test-all:
	py.test --cov=$(package) --cov-report=html --cov-report=term-missing  --verbose tests

tox:
	tox

coverage:
	coverage run --source $(package) setup.py test
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: install
	rm -f test1
	sphinx-apidoc  -f -P -o docs/test1 $(package)
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	pip install -r requirements.txt
	python setup.py install

flake8:
	flake8

pylint-quick:
	pylint --rcfile=.pylintrc $(package)  -E -r y

pylint:
	pylint --rcfile=".pylintrc" $(package)

dockerfile: clean
	docker build -t {{cookiecutter.docker_registry}}:v$(VERSION) .

dockerfile-canary: clean
	docker build -t {{cookiecutter.docker_registry}}:canary .
	docker push {{cookiecutter.docker_registry}}:canary

dockerfile-push: dockerfile
	docker push {{cookiecutter.docker_registry}}:v$(VERSION)

gen-ci:
	ffctl gen

check: pylint flake8 black-diff black-test

pyre:
	pyre

prepare: yapf gen-ci check

black:
	black -t py310 conf tests $(package)

black-test:
	black -t py310 conf tests $(package) --check

black-diff:
	black -t py310 conf tests $(package) --diff

rename:
	ack {{cookiecutter.varEnvPrefix}} -l | xargs -i{} sed -r -i "s/{{cookiecutter.varEnvPrefix}}/\{\{cookiecutter.varEnvPrefix\}\}/g" {}
	ack {{cookiecutter.project_slug}} -l | xargs -i{} sed -r -i "s/{{cookiecutter.project_slug}}/\{\{cookiecutter.project_slug\}\}/g" {}
	ack {{cookiecutter.baseclass}} -l | xargs -i{} sed -r -i "s/{{cookiecutter.baseclass}}/\{\{cookiecutter.baseclass\}\}/g" {}

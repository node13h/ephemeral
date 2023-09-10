VERSION := $(shell poetry version -s)

DOCKER_TAG := $(VERSION)
DOCKER_REPOSITORY := docker.io/alikov/ephemeral

SDIST_TARBALL = ephemeral-$(VERSION).tar.gz

APP_INSTANCE_URL = http://localhost:8080

.PHONY: all

all:
	true

.PHONY: clean develop reformat lint test typecheck all-tests build

clean:
	rm -rf dist/

develop:
	poetry install

reformat:
	poetry run black .
	poetry run isort .

lint:
	poetry run isort --check .
	poetry run black --check .
	poetry run flake8 --extend-ignore=E501

test:
	poetry run coverage run -m pytest -vv
	poetry run coverage report

typecheck:
	poetry run mypy .

all-tests: lint typecheck test

assets:
	yarnpkg install --modules-folder ./src/ephemeral/static/node_modules

build: assets
	poetry build

.PHONY: dev-server container-image container-image-push compose-up compose-down compose-ps e2e-test

dev-server:
	FLASK_APP=ephemeral.wsgi:application FLASK_ENV=development pipenv flask run

container-image:
	docker build -t $(DOCKER_REPOSITORY):$(DOCKER_TAG) --build-arg SDIST_TARBALL=$(SDIST_TARBALL) .

container-image-push: container-image
	docker push $(DOCKER_REPOSITORY):$(DOCKER_TAG)

compose-up:
	EPHEMERAL_IMAGE=$(DOCKER_REPOSITORY):$(DOCKER_TAG) EPHEMERAL_SECRET_KEY=hunter2 docker-compose up -d

compose-down:
	EPHEMERAL_SECRET_KEY=hunter2 docker-compose down -v --rmi local

compose-ps:
	EPHEMERAL_SECRET_KEY=hunter2 docker-compose ps

e2e-test:
	cd behave && pipenv sync && pipenv run behave -D app_base_url=$(APP_INSTANCE_URL)

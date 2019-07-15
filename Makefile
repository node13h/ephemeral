DOCKER_TAG := latest
DOCKER_REPOSITORY := docker.io/alikov/ephemeral

APP_INSTANCE_URL = http://localhost:8080

VERSION = $(shell cat VERSION)

.PHONY: assets clean sdist dev-server test develop build-image push-image compose-build compose-up compose-down compose-ps e2e-test release-start release-finish release publish

all:
	true

assets:
	yarnpkg install --modules-folder ./ephemeral/static/node_modules

clean:
	rm -rf dist
	rm -rf ./ephemeral/static/node_modules

sdist: assets dist/ephemeral-$(VERSION).tar.gz

dist/ephemeral-$(VERSION).tar.gz:
	python3 setup.py sdist

publish:
	twine upload dist/*

dev-server:
	FLASK_APP=ephemeral.wsgi:application FLASK_ENV=development flask run

test:
	pytest

develop:
	pip3 install -r requirements_dev.txt

build-image:
	docker build -t $(DOCKER_REPOSITORY):$(DOCKER_TAG) .

push-image: build-image
	docker push $(DOCKER_REPOSITORY):$(DOCKER_TAG)

compose-build:
	EPHEMERAL_SECRET_KEY=hunter2 docker-compose build

compose-up:
	EPHEMERAL_SECRET_KEY=hunter2 docker-compose up -d

compose-down:
	EPHEMERAL_SECRET_KEY=hunter2 docker-compose down -v

compose-ps:
	EPHEMERAL_SECRET_KEY=hunter2 docker-compose ps

e2e-test:
	cd behave && pipenv sync && pipenv run behave -D app_base_url=$(APP_INSTANCE_URL)

release-start:
	bash release.sh start

release-finish:
	bash release.sh finish

release: release-start release-finish

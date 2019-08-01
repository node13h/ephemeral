PROJECT := ephemeral
VERSION = $(shell cat VERSION)
SDIST_TARBALL = dist/$(PROJECT)-$(VERSION).tar.gz

DOCKER_TAG := latest
DOCKER_REPOSITORY := docker.io/alikov/ephemeral

APP_INSTANCE_URL = http://localhost:8080

export RELEASE_REMOTE := origin
export RELEASE_PUBLISH := 0

.PHONY: all assets clean develop shell lint build test update-deps dev-server build-image push-image compose-build compose-up compose-down compose-ps e2e-test release-start release-finish sdist publish

all:
	true

assets:
	yarnpkg install --modules-folder ./ephemeral/static/node_modules

clean:
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf ./ephemeral/static/node_modules
	rm -f Pipfile.lock
	-pipenv --rm

develop:
	pipenv install --dev

shell:
	pipenv shell

lint:
	pipenv run flake8 --max-line-length=119 --exclude=.git,__pycache__,.tox,.eggs,*.egg

build:
	python3 setup.py build

test: lint build
	pipenv run pytest --verbose

update-deps:
	pipenv update

dev-server:
	FLASK_APP=ephemeral.wsgi:application FLASK_ENV=development pipenv flask run

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

release-start: test
	pipenv run lase $${RELEASE_REMOTE:+--remote "$${RELEASE_REMOTE}"} start $${RELEASE_VERSION:+--version "$${RELEASE_VERSION}"}

release-finish:
	pipenv run lase $${RELEASE_REMOTE:+--remote "$${RELEASE_REMOTE}"} finish
	if [ "$${RELEASE_PUBLISH}" -eq 1 ]; then $(MAKE) -f $(lastword $(MAKEFILE_LIST)) publish; fi

sdist: assets $(SDIST_TARBALL)

$(SDIST_TARBALL):
	python3 setup.py sdist

publish: test $(SDIST_TARBALL)
	pipenv run twine upload $(SDIST_TARBALL)

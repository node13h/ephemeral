DOCKER_TAG := latest
DOCKER_REPOSITORY := docker.io/alikov/ephemeral

APP_INSTANCE_URL = http://localhost:8080

VERSION = $(shell cat VERSION)

.PHONY: all assets clean develop shell lint test update-deps dev-server build-image push-image compose-build compose-up compose-down compose-ps e2e-test release-start release-finish release sdist publish

all:
	true

assets:
	yarnpkg install --modules-folder ./ephemeral/static/node_modules

clean:
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf ./ephemeral/static/node_modules
	pipenv --rm || true

develop:
	pipenv install --dev

shell:
	pipenv shell

lint:
	pipenv run flake8 --max-line-length=119 --exclude=.git,__pycache__,.tox,.eggs,*.egg

test: lint
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
	pipenv run lase --remote origin start $${RELEASE_VERSION:+--version "$${RELEASE_VERSION}"}

release-finish:
	pipenv run lase --remote origin finish

release: release-start release-finish

sdist: assets dist/ephemeral-$(VERSION).tar.gz

dist/ephemeral-$(VERSION).tar.gz:
	python3 setup.py sdist

publish: test dist/ephemeral-$(VERSION).tar.gz
	pipenv run twine upload dist/ephemeral-$(VERSION).tar.gz:


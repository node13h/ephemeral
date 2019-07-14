DOCKER_TAG := latest
DOCKER_REPOSITORY := docker.io/alikov/ephemeral
APP_INSTANCE_URL = http://localhost:8080

.PHONE: assets sdist dev-server test develop build-image push-image

all:
	true

assets:
	yarnpkg install --modules-folder ./ephemeral/static/node_modules

sdist: assets
	python3 setup.py sdist

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

compose-up:
	EPHEMERAL_SECRET_KEY=hunter2 docker-compose up

compose-down:
	EPHEMERAL_SECRET_KEY=hunter2 docker-compose down -v

e2e-test:
	cd behave && pipenv run behave -D app_base_url=$(APP_INSTANCE_URL)

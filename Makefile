.PHONE: assets sdist dev-server

all:
	true

assets:
	yarnpkg install --modules-folder ./ephemeral/static/node_modules

sdist: assets
	python3 setup.py sdist

dev-server:
	FLASK_APP=ephemeral.wsgi:application FLASK_ENV=development flask run

.PHONE: assets sdist

all:
	true

assets:
	yarnpkg install --modules-folder ./ephemeral/static/node_modules

sdist: assets
	python3 setup.py sdist

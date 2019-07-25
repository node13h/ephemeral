# ephemeral - Self-destructing messages

Ephemeral is a web application for sharing short messages. Messages can be opened
only once, giving an instant feedback to recipient on whether the message was
compromised(read by someone else) or not. This makes the app a reasonably secure,
and convenient way to share secrets.

## Highlights

- Simple, easy-to-audit code
- Messages are encrypted at rest


## Installing

```sh
pip install ephemeral
```

After installation you can use the `ephemeral.sh` command to start the
application (see below).


## Running

Always put this application behind an HTTPS-terminating reverse proxy when exposing to
public networks!

Ephemeral uses Redis as the data store. Assuming Redis is running on `localhost`,

```sh
EPHEMERAL_REDIS_HOST=localhost EPHEMERAL_SECRET_KEY=hunter2 ephemeral.sh 0.0.0.0:8080
```

will start the application listning on port 8080 on all network interfaces.

Point your browser at http://localhost:8080/add to add a message.


## Developing

Prerequisites:

- Python 3
- [pipenv](https://docs.pipenv.org/en/latest/#install-pipenv-today)

Initialize a virtualenv with dev dependencies installed:

```sh
make develop
```


### Project dependencies

Project dependencies shoud always be specified in `setup.py` using the
[compatible release](https://www.python.org/dev/peps/pep-0440/#compatible-release)
notation.


### Updating dependencies in virtualenv

Run the following after updating `setup.py`

```sh
make update-deps
```


### Installing development dependencies

Replace `<PACKAGE>` with the actual name, and `<VERSION>` with the MAJOR.MINOR
(or MAJOR.MINOR.PATCH for versions below 1.0.0) version of the package.
[Read more on compatible releases](https://www.python.org/dev/peps/pep-0440/#compatible-release).

```sh
pipenv install --dev <PACKAGE>~=<VERSION>
```


### Running unit-tests

```sh
make test
```


### Starting a development instance of the application

Start the application in development mode with debugging enabled:

```sh
make dev-server
```


### Starting/stopping a development Docker stack

The development Docker (Compose) stack includes Redis container and an application
container built from source.

Prerequisites:

- Docker
- docker-compose

(Re)Build the application image, start a stack in background, and show running containers:

```sh
make compose-build

make compose-up

make compose-ps
```

Stop and destroy running stack:

```sh
make compose-down
```


### Running E2E tests

Start a stack and run Behave tests against it:

```sh
make compose-up

make e2e-test
```


### Starting a release

Variables:

- `RELEASE_REMOTE` set to the name of the Git remote. Set to empty to disable pushes to
remote. Default value: `origin`
- `RELEASE_VERSION` override the release version, or leave empty to release the current
snapshot (`-SNAPSHOT` will be stripped off). Empty by default

```sh
make release-start
```


### Finishing a release

Variables:

- `RELEASE_REMOTE` set to the name of the Git remote. Set to empty to disable pushes to
remote. Default value: `origin`
- `RELEASE_PUBLISH` set to `1` to enable publishing of the sdist tarball after the release`

```sh
make release-finish
```

`release-finish` will leave the release Git tag checked out on completion.


### Building and publishing the source distribution:

```sh
make publish
```

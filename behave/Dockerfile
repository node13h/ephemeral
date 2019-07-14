FROM python:3.7.4-alpine3.10
COPY Pipfile /
COPY Pipfile.lock /
RUN apk add --no-cache make && pip install pipenv==2018.11.26 && pipenv sync
ENTRYPOINT ["pipenv", "run", "behave"]

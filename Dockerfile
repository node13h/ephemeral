FROM python:3.7.5-alpine3.10

COPY . /dist

WORKDIR /dist

RUN apk add --no-cache gcc g++ make libffi-dev openssl-dev && python3 setup.py install && rm -rf -- /dist/* && apk del gcc g++ make libffi-dev openssl-dev

EXPOSE 8080

ENTRYPOINT ["ephemeral.sh", "0.0.0.0:8080"]

FROM python:3.11.5-alpine3.18

ARG SDIST_TARBALL

COPY dist/${SDIST_TARBALL} /dist/${SDIST_TARBALL}

RUN pip3 install dist/${SDIST_TARBALL}

EXPOSE 8080

ENTRYPOINT ["ephemeral.sh", "0.0.0.0:8080"]

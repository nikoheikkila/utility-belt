FROM python:3.7-alpine
LABEL maintainer="Niko Heikkilä <yo@nikoheikkila.fi>"

ENV PIPENV_CACHE_DIR=/cache

RUN apk add --update --no-cache \
    gcc \
    g++ \
    libxslt-dev \
    && pip install --no-cache-dir --upgrade pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system && rm -rf /cache

COPY scripts/ .

ENTRYPOINT [ "python" ]

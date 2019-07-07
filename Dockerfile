FROM python:3.7-alpine

LABEL maintainer="Niko Heikkilä <yo@nikoheikkila.fi>"

ARG PYTHON_ENV=production

ENV PYTHON_ENV=${PYTHON_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIPENV_HIDE_EMOJIS=true \
    PIPENV_COLORBLIND=true \
    PIPENV_NOSPIN=true \
    PIPENV_CACHE_DIR=/cache

# System dependencies
RUN apk --no-cache add \
    bash \
    build-base \
    curl \
    gcc \
    g++ \
    libffi-dev \
    libxslt-dev \
    linux-headers \
    musl-dev

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv \
    && pipenv install $(test "$PYTHON_ENV" == production || echo "--dev") --deploy --system --ignore-pipfile \
    && rm -rf /cache

COPY scripts/ .

ENTRYPOINT [ "python" ]

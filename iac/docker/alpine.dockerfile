#
# Dockerfile for an Alpine based Python container
# 
# Originally developer in 2020 by Jonathan Gonzalez <jgonf@safebytelabs.com>
# Licensed under the Mozilla Public License 2.0
#

FROM python:3.14.2-alpine3.23
LABEL maintainer="Jonathan Gonzalez <ea1het@ea1het.com>"
ARG GIT_BRANCH

ENV RUN_DEPENDENCIES="python3 py3-pip curl"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1
ENV POETRY_HOME="/root/.local" POETRY_VERSION=1.8.3

# Let service stop gracefully
STOPSIGNAL SIGQUIT

# Install system dependencies and Poetry
RUN apk add --no-cache $RUN_DEPENDENCIES \
    && apk add --no-cache --virtual .build-deps build-base \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && rm -rf /root/.cache               \
    && rm -rf /var/cache/apk/*

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory
WORKDIR /opt/app

# Copy dependency definitions
COPY ./pyproject.toml ./poetry.lock ./

# Install dependencies with Poetry (system site-packages)
RUN poetry install --no-root --no-dev \
    && apk del .build-deps \
    && rm -rf /root/.cache/pypoetry

# Copy the application source code and entrypoint into /opt/app
COPY ./src/ ./
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Ensure local sources are importable
ENV PYTHONPATH=/opt/app

# Set the port environment variable, default to 9000 if not set
ENV GUNIPORT=9000

# Use the unified entrypoint to start API or worker modes
ENTRYPOINT ["/entrypoint.sh"]

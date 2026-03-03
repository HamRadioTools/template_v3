# ---- builder ----
FROM python:3.14.2-alpine3.23 AS builder
ENV POETRY_HOME="/root/.local" POETRY_VERSION=1.8.3
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /opt/app

RUN apk add --no-cache curl \
    && apk add --no-cache --virtual .build-deps build-base \
    && curl -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml poetry.lock ./

RUN poetry export -f requirements.txt --without-hashes --without dev -o /tmp/requirements.txt \
    && pip wheel --no-cache-dir --wheel-dir /wheels -r /tmp/requirements.txt

# ---- runtime ----
FROM python:3.14.2-alpine3.23
WORKDIR /opt/app
COPY --from=builder /wheels /wheels
COPY --from=builder /tmp/requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --find-links=/wheels -r /tmp/requirements.txt \
    && rm -rf /wheels /tmp/requirements.txt

COPY ./src/ /opt/app/
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONPATH=/opt/app
ENV GUNIPORT=9000

STOPSIGNAL SIGQUIT
ENTRYPOINT ["/entrypoint.sh"]

ARG IMAGE

FROM ${IMAGE} AS builder

RUN apk add --quiet --no-cache \
    build-base \
    libffi-dev \
    openssh \
    git \
    gcc

RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

RUN pip install poetry==1.8.0

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=ssh poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM ${IMAGE} AS runtime

RUN apk --quiet --no-cache add ca-certificates \
    && rm -rf /var/cache/apk/*

# Add certificates
# COPY docker/postgres-ca-certificate.crt /usr/local/share/ca-certificates/
# RUN chmod 644 /usr/local/share/ca-certificates/*.crt && update-ca-certificates

WORKDIR /app
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="$PYTHONPATH"
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
RUN python -m compileall /app

ENTRYPOINT ["/app/.venv/bin/uvicorn", "ory_test.main:app", "--host", "0.0.0.0", "--port", "8000"]
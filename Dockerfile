FROM python:3.12-slim-trixie AS uvbin
# Use the official Python 3.12 slim image for a lightweight base.
FROM spatialetl:0.2.2 AS python-builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends git openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Trust GitHub's host key
RUN mkdir -p -m 0700 /root/.ssh \
    && ssh-keyscan github.com >> /root/.ssh/known_hosts

# Prevent Python from writing .pyc files to disk and enable unbuffered logging.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENV UV_PROJECT_ENVIRONMENT=/app/.venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

ENV UV_NO_DEV=1
ENV UV_SYSTEM_PYTHON=1
ENV UV_COMPILE_BYTECODE=1

# Set the working directory to /app
WORKDIR /app

# Copy the entire project into the container.
COPY . .

RUN --mount=type=ssh --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
 uv pip install . --python /app/.venv/bin/python

FROM spatialetl:0.2.2 AS prod

# Copy the environment, but not the source code
COPY --from=python-builder --chown=app:app /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"


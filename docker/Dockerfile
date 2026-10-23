# Image for this project. Build it with: python docker/build_image.py
#
# Secrets (.env) are never copied into the image. run_container.py passes
# them in when the container starts.

ARG PYTHON_VERSION=3.13
FROM python:${PYTHON_VERSION}-slim

# uv installs the packages listed in uv.lock
ARG UV_VERSION=0.12.24
COPY --from=ghcr.io/astral-sh/uv:${UV_VERSION} /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# 1. Install packages first, so this slow step is cached until uv.lock changes
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-dev --no-install-project

# 2. Copy the project code
COPY . .
RUN uv sync --locked --no-dev

# Run as a normal user, not root
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

CMD ["python", "main.py"]

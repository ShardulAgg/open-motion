# syntax = docker/dockerfile:1.4

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-slim AS builder

# Install build-essential for C++ compiler
RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt  --default-timeout=300

COPY ./ .

FROM builder as dev-envs

RUN apt-get update && \
    apt-get install -y --no-install-recommends git

RUN useradd -s /bin/bash -m vscode && \
    groupadd docker && \
    usermod -aG docker vscode


COPY --from=gloursdocker/docker / /

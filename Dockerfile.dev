# syntax=docker/dockerfile:1.4

# Create requirements.txt 
FROM python:3.13-slim as builder

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Install exporter plugin
RUN poetry self add poetry-plugin-export

# Copy deps
COPY pyproject.toml poetry.lock ./

# Write requirements file
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Install
FROM python:3.13-slim

WORKDIR /app

# Copy requirements from build stage
COPY --from=builder /app/requirements.txt . 

# Install with pip with cache
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Copy application code
COPY src src

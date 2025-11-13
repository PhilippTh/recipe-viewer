# Multi-stage build following UV best practices
# Build stage
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

# Enable bytecode compilation for better performance
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project into `/app`
WORKDIR /app

# Install dependencies first (better caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then copy the rest of the project and install it
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# Production stage
FROM ghcr.io/astral-sh/uv:python3.12-alpine

# Install gettext for translations
RUN apk add --no-cache gettext

# Create non-root user for security (using Alpine's adduser/addgroup)
RUN addgroup -g 1000 nonroot \
 && adduser -D -u 1000 -G nonroot nonroot

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=recipe_viewer.settings

# Set working directory
WORKDIR /app

# Copy the application from the builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Create directories for media and static files with proper permissions
RUN mkdir -p /app/media /app/static /app/data \
    && chown -R nonroot:nonroot /app/media /app/static /app/data \
    && chmod +x /app/entrypoint.sh

# Use the non-root user to run our application
USER nonroot

# Expose port
EXPOSE 8000

# Run entrypoint script
ENTRYPOINT ["./entrypoint.sh"]

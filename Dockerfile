FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy application code
COPY . .

# Run migrations and collect static files
RUN uv run python manage.py migrate
RUN uv run python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
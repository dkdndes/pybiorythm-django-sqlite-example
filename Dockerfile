FROM python:3.12-slim

# Install Git (required for uv to install dependencies from Git repositories)
RUN apt-get update && apt-get install -y git && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Create virtual environment and install dependencies
RUN uv venv
RUN uv pip install --no-cache-dir django>=5.2.5 python-dateutil>=2.8.0 python-dotenv>=1.0.0 "biorythm @ git+https://github.com/dkdndes/pybiorythm.git"

# Copy application code
COPY . .

# Run migrations and collect static files
RUN uv run python manage.py migrate
RUN uv run python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
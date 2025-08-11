#!/bin/bash

# PyBiorythm Django SQLite Example Setup Script
# This script sets up the development environment and loads sample data

set -e  # Exit on any error

echo "🚀 Setting up PyBiorythm Django SQLite Example..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

echo "🔧 Creating virtual environment and installing dependencies..."
uv venv
source .venv/bin/activate
uv sync

echo "🗄️ Running database migrations..."
uv run python manage.py migrate

echo "👤 Creating sample data..."
uv run python manage.py load_biorhythm_data \
    --name "Demo User" \
    --birthdate "1990-01-15" \
    --days 365 \
    --email "demo@example.com" \
    --notes "Sample data for demonstration"

echo "🔑 Create a superuser account (press Ctrl+C to skip):"
echo "Username: admin"
echo "Email: admin@example.com" 
echo "Password: admin123"
echo ""
uv run python manage.py createsuperuser --noinput \
    --username admin \
    --email admin@example.com || echo "Superuser creation skipped or already exists"

echo "✅ Setup complete!"
echo ""
echo "🌐 To start the development server:"
echo "   source .venv/bin/activate"
echo "   uv run python manage.py runserver"
echo ""
echo "📋 Access the application:"
echo "   - Django Admin: http://127.0.0.1:8000/admin/"
echo "   - API: http://127.0.0.1:8000/api/"
echo ""
echo "🔐 Admin credentials:"
echo "   Username: admin"
echo "   Password: admin123"
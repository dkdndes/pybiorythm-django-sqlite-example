# PyBiorythm Django SQLite Integration Example

A complete Django application demonstrating how to integrate the [PyBiorythm](https://github.com/dkdndes/pybiorythm) library with SQLite for biorhythm data storage and management.

## 🌟 Features

- **SQLite Database Integration** with Django ORM
- **PyBiorythm Library Integration** for real biorhythm calculations
- **Database Models** for storing biorhythm data, people, and calculations
- **Django Admin Interface** for data management
- **Management Commands** for bulk data loading
- **Comprehensive Data Models** with relationships and validation
- **Performance Optimized** with database indexes

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Database Schema](#database-schema)
- [Management Commands](#management-commands)
- [Django Admin](#django-admin)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/pybiorythm-django-sqlite-example.git
   cd pybiorythm-django-sqlite-example
   ```

2. **Set up virtual environment and install dependencies**
   ```bash
   # Install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Create virtual environment and install dependencies
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
   ```

4. **Run migrations**
   ```bash
   uv run python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   uv run python manage.py createsuperuser
   ```

6. **Load sample data**
   ```bash
   uv run python manage.py load_biorhythm_data --name "Test User" --birthdate "1990-01-15" --days 365
   ```

7. **Start the development server**
   ```bash
   uv run python manage.py runserver
   ```

8. **Access the application**
   - Django Admin: http://127.0.0.1:8000/admin/
   - API: http://127.0.0.1:8000/api/

## 📦 Installation

### Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation with uv

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync
```

### Dependencies

This project uses the following key dependencies:

- **Django** 5.2.5+ - Web framework
- **PyBiorythm** - Real biorhythm calculations from GitHub
- **django-extensions** - Enhanced Django management commands
- **python-dateutil** - Date/time utilities

## 💻 Usage

### Basic Usage

1. **Create a person and calculate biorhythms**:
   ```bash
   uv run python manage.py load_biorhythm_data --name "John Doe" --birthdate "1985-03-20" --days 180
   ```

2. **Access Django Admin** to view and manage data:
   ```
   http://127.0.0.1:8000/admin/
   ```

3. **Query data programmatically**:
   ```python
   from biorhythm_data.models import Person, BiorhythmData
   
   # Get a person
   person = Person.objects.get(name="John Doe")
   
   # Get their biorhythm data
   data = BiorhythmData.objects.filter(person=person).order_by('date')
   
   # Get critical days
   critical_days = data.filter(
       Q(is_physical_critical=True) |
       Q(is_emotional_critical=True) |
       Q(is_intellectual_critical=True)
   )
   ```

### Advanced Usage

#### Custom Date Ranges
```bash
uv run python manage.py load_biorhythm_data \
    --name "Jane Smith" \
    --birthdate "1992-07-10" \
    --start-date "2024-01-01" \
    --end-date "2024-12-31"
```

#### Bulk Data Processing
```bash
# Load multiple people from a CSV file
uv run python manage.py load_bulk_biorhythm_data people.csv
```

## 🗄️ Database Schema

### Models Overview

#### Person Model
Stores individual person information and biorhythm metadata.

```python
class Person(models.Model):
    name = models.CharField(max_length=200)
    birthdate = models.DateField()
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### BiorhythmData Model
Stores calculated biorhythm values for specific dates.

```python
class BiorhythmData(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    date = models.DateField()
    days_alive = models.IntegerField()
    physical = models.FloatField()         # Range: -1.0 to 1.0
    emotional = models.FloatField()        # Range: -1.0 to 1.0
    intellectual = models.FloatField()     # Range: -1.0 to 1.0
    is_physical_critical = models.BooleanField(default=False)
    is_emotional_critical = models.BooleanField(default=False)
    is_intellectual_critical = models.BooleanField(default=False)
```

#### BiorhythmCalculation Model
Tracks calculation metadata and parameters.

```python
class BiorhythmCalculation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    days_calculated = models.IntegerField()
    calculation_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
```

### Database Indexes

Optimized indexes for common queries:
- `person_id + date` (composite index)
- `date` (for date range queries)
- `is_*_critical` (for critical day lookups)

## 🛠️ Management Commands

### load_biorhythm_data

Load biorhythm data for a person into the database.

```bash
uv run python manage.py load_biorhythm_data [OPTIONS]
```

**Options:**
- `--name` - Person's name (required)
- `--birthdate` - Birth date in YYYY-MM-DD format (required)
- `--days` - Number of days to calculate (default: 365)
- `--start-date` - Start date for calculations (default: today)
- `--email` - Person's email address (optional)
- `--notes` - Calculation notes (optional)

**Examples:**
```bash
# Basic usage
uv run python manage.py load_biorhythm_data --name "Alice Cooper" --birthdate "1988-12-25"

# With custom parameters
uv run python manage.py load_biorhythm_data \
    --name "Bob Dylan" \
    --birthdate "1975-05-15" \
    --days 730 \
    --email "bob@example.com" \
    --notes "Two year analysis"

# Specific date range
uv run python manage.py load_biorhythm_data \
    --name "Carol King" \
    --birthdate "1990-08-30" \
    --start-date "2024-01-01" \
    --days 365
```

### Data Export Commands

```bash
# Export data to CSV
uv run python manage.py export_biorhythm_data --person-id 1 --format csv

# Export data to JSON
uv run python manage.py export_biorhythm_data --person-id 1 --format json
```

## 👑 Django Admin

The Django admin interface provides a comprehensive view of all biorhythm data:

### Features
- **Person Management** - Add, edit, and delete people
- **Biorhythm Data Browser** - View calculated biorhythm values
- **Calculation History** - Track all calculations performed
- **Data Filtering** - Filter by date ranges, people, critical days
- **Bulk Operations** - Perform batch operations on data

### Admin Customizations
- **Enhanced List Views** with filtering and search
- **Custom Actions** for bulk data operations
- **Inline Editing** for related models
- **Data Validation** with custom form validators

## 📖 API Documentation

### Models API

#### Person
```python
# Create a person
person = Person.objects.create(
    name="Example User",
    birthdate="1990-01-01",
    email="user@example.com"
)

# Query methods
Person.objects.get_active_people()
Person.objects.with_recent_calculations()
```

#### BiorhythmData
```python
# Get data for a person
data = BiorhythmData.objects.filter(person=person)

# Get critical days
critical = BiorhythmData.objects.get_critical_days(person=person)

# Get data by date range
range_data = BiorhythmData.objects.get_date_range(
    person=person,
    start_date="2024-01-01",
    end_date="2024-12-31"
)
```

### Calculation Functions

```python
from biorhythm_data.utils import calculate_biorhythm_range

# Calculate biorhythm for a date range
results = calculate_biorhythm_range(
    birthdate="1990-01-01",
    start_date="2024-01-01",
    days=365
)
```

## 🔧 Configuration

### Django Settings

Key settings in `biorhythm_storage/settings.py`:

```python
# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PyBiorythm specific settings
BIORHYTHM_DEFAULT_DAYS = 365
BIORHYTHM_MAX_DAYS = 3650
BIORHYTHM_BATCH_SIZE = 1000
```

### Environment Variables

Create a `.env` file for local development:

```bash
DEBUG=True
SECRET_KEY=your-secret-key-here
BIORHYTHM_DEFAULT_DAYS=365
BIORHYTHM_MAX_CALCULATION_DAYS=3650
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
uv run python manage.py test

# Run with coverage
uv run coverage run --source='.' manage.py test
uv run coverage report
uv run coverage html  # Generates HTML coverage report
```

### Test Structure
- **Model Tests** - Test model methods and validation
- **Management Command Tests** - Test data loading commands
- **Admin Tests** - Test admin interface functionality
- **Integration Tests** - Test PyBiorythm integration

## 📊 Performance Considerations

### Database Optimization
- **Indexes** on frequently queried fields
- **Batch Processing** for large data sets
- **Connection Pooling** for production deployments

### Memory Management
- **Chunked Processing** for large calculations
- **Lazy Loading** of related objects
- **Query Optimization** with `select_related` and `prefetch_related`

## 🐳 Docker Support

### Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    environment:
      - DEBUG=1
```

## 🚀 Deployment

### Production Considerations

1. **Database** - Consider PostgreSQL for production
2. **Static Files** - Configure static file serving
3. **Security** - Update SECRET_KEY and security settings
4. **Performance** - Enable caching and optimization

### Environment Setup
```bash
# Production settings
export DEBUG=False
export SECRET_KEY="your-production-secret-key"
export ALLOWED_HOSTS="yourdomain.com"

# Database URL for production
export DATABASE_URL="postgresql://user:pass@localhost/dbname"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
uv sync --extra dev

# Run tests before committing
uv run python manage.py test
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- **[PyBiorythm](https://github.com/dkdndes/pybiorythm)** - Core biorhythm calculation library
- **[PyBiorythm Django API Server](https://github.com/your-username/pybiorythm-django-api-server-example)** - REST API server example
- **[PyBiorythm Django Dashboard](https://github.com/your-username/pybiorythm-django-dashboard-example)** - Visualization dashboard example

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/pybiorythm-django-sqlite-example/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/pybiorythm-django-sqlite-example/discussions)
- **Documentation**: [Wiki](https://github.com/your-username/pybiorythm-django-sqlite-example/wiki)

## 🙏 Acknowledgments

- **PyBiorythm Library** by [dkdndes](https://github.com/dkdndes)
- **Django Framework** by the Django Software Foundation
- **Contributors** and community members who helped improve this example

---

**Made with ❤️ for the PyBiorythm community**
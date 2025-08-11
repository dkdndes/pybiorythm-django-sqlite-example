#!/usr/bin/env python
"""
Quick start script for PyBiorythm Django SQLite Example

This script demonstrates basic usage of the biorhythm models and data loading.
"""

import os
import sys
from datetime import date, timedelta

import django

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "biorhythm_storage.settings")
django.setup()

from django.core.management import call_command  # noqa: E402

from biorhythm_data.models import BiorhythmCalculation, BiorhythmData, Person  # noqa: E402


def main():
    print("🌟 PyBiorythm Django SQLite Example - Quick Start")
    print("=" * 50)

    # Run migrations if needed
    print("🔧 Running migrations...")
    call_command("migrate", verbosity=0)

    # Create a sample person if not exists
    person_name = "Quick Start Demo"
    person, created = Person.objects.get_or_create(
        name=person_name, defaults={"birthdate": date(1990, 5, 15), "email": "demo@example.com"}
    )

    if created:
        print(f"👤 Created person: {person.name}")
    else:
        print(f"👤 Using existing person: {person.name}")

    # Load biorhythm data if not exists
    data_count = BiorhythmData.objects.filter(person=person).count()

    if data_count == 0:
        print("📊 Loading biorhythm data...")
        call_command(
            "load_biorhythm_data",
            "--name",
            person.name,
            "--birthdate",
            person.birthdate.strftime("%Y-%m-%d"),
            "--days",
            "90",
            "--notes",
            "Quick start demo data",
        )
        data_count = BiorhythmData.objects.filter(person=person).count()
        print(f"✅ Loaded {data_count} data points")
    else:
        print(f"📊 Using existing {data_count} data points")

    # Display some statistics
    print("\n📈 Quick Statistics:")
    print("-" * 30)

    # Get recent data
    recent_data = BiorhythmData.objects.filter(person=person).order_by("-date")[:5]

    if recent_data:
        print(f"📅 Most recent date: {recent_data[0].date}")
        print(f"🏃 Physical: {recent_data[0].physical:.3f}")
        print(f"💭 Emotional: {recent_data[0].emotional:.3f}")
        print(f"🧠 Intellectual: {recent_data[0].intellectual:.3f}")

        # Critical days
        critical_days = (
            BiorhythmData.objects.filter(person=person, date__gte=date.today() - timedelta(days=30))
            .filter(
                models.Q(is_physical_critical=True)
                | models.Q(is_emotional_critical=True)
                | models.Q(is_intellectual_critical=True)
            )
            .count()
        )

        print(f"⚠️  Critical days (last 30): {critical_days}")

    # Display model information
    print("\n🗄️  Database Info:")
    print("-" * 30)
    print(f"👥 Total people: {Person.objects.count()}")
    print(f"📊 Total data points: {BiorhythmData.objects.count()}")
    print(f"🔢 Total calculations: {BiorhythmCalculation.objects.count()}")

    print("\n🚀 Next Steps:")
    print("-" * 30)
    print("1. Start the development server:")
    print("   uv run python manage.py runserver")
    print("\n2. Access the Django Admin:")
    print("   http://127.0.0.1:8000/admin/")
    print("\n3. Create a superuser:")
    print("   uv run python manage.py createsuperuser")
    print("\n4. Explore the API:")
    print("   http://127.0.0.1:8000/api/")

    print("\n✨ Quick start completed successfully!")


if __name__ == "__main__":
    # Import models here to avoid circular imports
    from django.db import models

    main()

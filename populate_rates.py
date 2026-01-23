import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from core.models import ScrapCategory

def populate_rates():
    initial_data = [
        {'name': 'Newspaper', 'rate': 14.00},
        {'name': 'Cardboard', 'rate': 5.00},
        {'name': 'Iron', 'rate': 26.00},
        {'name': 'Plastic', 'rate': 12.00},
        {'name': 'Brass', 'rate': 305.00},
        {'name': 'Copper', 'rate': 420.00},
        {'name': 'E-Waste', 'rate': 15.00},
        {'name': 'Aluminium', 'rate': 105.00},
    ]

    for item in initial_data:
        category, created = ScrapCategory.objects.get_or_create(
            name=item['name'],
            defaults={'rate_per_kg': item['rate']}
        )
        if created:
            print(f"Created category: {item['name']}")
        else:
            print(f"Category already exists: {item['name']}")

if __name__ == '__main__':
    populate_rates()

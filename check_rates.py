import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from core.models import ScrapCategory

def check_rates():
    count = ScrapCategory.objects.count()
    print(f"Total ScrapCategories: {count}")
    for cat in ScrapCategory.objects.all():
        print(f"- {cat.name}: {cat.rate_per_kg}")

if __name__ == '__main__':
    check_rates()

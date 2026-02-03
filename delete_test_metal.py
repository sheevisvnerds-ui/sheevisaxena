import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from core.models import ScrapCategory

def delete_test_metal():
    try:
        category = ScrapCategory.objects.get(name="Test Metal")
        category.delete()
        print("Successfully deleted 'Test Metal' category.")
    except ScrapCategory.DoesNotExist:
        print("'Test Metal' category not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    delete_test_metal()

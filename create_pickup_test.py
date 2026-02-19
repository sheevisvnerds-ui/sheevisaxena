
import os
import django
from django.utils import timezone
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from core.models import User, PickupRequest, ScrapCategory

def create_test_pickup():
    customer = User.objects.get(username='test_customer')
    agent = User.objects.get(username='test_agent')
    category = ScrapCategory.objects.first()
    
    if not category:
        category = ScrapCategory.objects.create(name="Mix Scrap", rate_per_kg=15.0)

    # Create Assigned Pickup
    pickup, created = PickupRequest.objects.get_or_create(
        customer=customer,
        status=PickupRequest.Status.ASSIGNED,
        defaults={
            'agent': agent,
            'scheduled_date': timezone.now() + timezone.timedelta(days=1),
            'address': 'Test Address',
            'estimated_weight': 10.0,
            'scrap_category': category
        }
    )
    if created:
        print(f"Created pickup #{pickup.id}")
    else:
        print(f"Pickup #{pickup.id} already exists")

if __name__ == "__main__":
    create_test_pickup()

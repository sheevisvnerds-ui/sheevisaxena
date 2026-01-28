import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from core.models import PickupRequest, User

# Get the first agent user (assuming the user is logged in as one)
# Or just list all assigned pickups
print(f"Current Server Date: {timezone.now().date()}")

assigned = PickupRequest.objects.filter(status=PickupRequest.Status.ASSIGNED).order_by('scheduled_date')

if not assigned.exists():
    print("No assigned pickups found.")
else:
    for p in assigned:
        p_date = p.scheduled_date.date()
        is_today = p_date == timezone.now().date()
        is_future = p_date > timezone.now().date()
        print(f"Pickup {p.id}: {p.scheduled_date} (Date: {p_date}) - Is Today? {is_today}, Is Future? {is_future}, Agent: {p.agent}")

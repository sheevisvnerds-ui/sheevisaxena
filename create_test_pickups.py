import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from core.models import PickupRequest, User, ScrapCategory

# Get users
agent = User.objects.filter(role='AGENT').first()
customer = User.objects.filter(role='CUSTOMER').first()

if not agent:
    print("No agent found. Creating one.")
    agent = User.objects.create_user(username='agent1', password='password123', role='AGENT')

if not customer:
    print("No customer found. Creating one.")
    customer = User.objects.create_user(username='customer1', password='password123', role='CUSTOMER')

# Ensure categories exist
if not ScrapCategory.objects.exists():
    ScrapCategory.objects.create(name="Newspaper", rate_per_kg=12)
    ScrapCategory.objects.create(name="Iron", rate_per_kg=25)

category = ScrapCategory.objects.first()

# Create Today's Task
today = timezone.now()
p1 = PickupRequest.objects.create(
    customer=customer,
    agent=agent,
    address="123 Today Street, Tech Park",
    scheduled_date=today,
    estimated_weight=15.0,
    status=PickupRequest.Status.ASSIGNED
)
print(f"Created Today's Pickup: {p1.id} for {p1.scheduled_date}")

# Create Future Task
tomorrow = today + timedelta(days=1)
p2 = PickupRequest.objects.create(
    customer=customer,
    agent=agent,
    address="456 Future Lane, Suburbs",
    scheduled_date=tomorrow,
    estimated_weight=30.0,
    status=PickupRequest.Status.ASSIGNED
)
print(f"Created Future Pickup: {p2.id} for {p2.scheduled_date}")

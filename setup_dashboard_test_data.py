import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import PickupRequest, ScrapCategory

User = get_user_model()

def setup_dashboard_data():
    print("Setting up Dashboard Test Data...")

    # Ensure Users Exist
    customer = User.objects.get(username='test_customer')
    agent = User.objects.get(username='test_agent')
    
    # Ensure Category
    category, _ = ScrapCategory.objects.get_or_create(name='Iron', defaults={'rate_per_kg': 30.0})

    # 1. Pending Request (Unassigned)
    PickupRequest.objects.create(
        customer=customer,
        status=PickupRequest.Status.PENDING,
        scheduled_date=timezone.now() + timedelta(days=1),
        address="456 Pending Lane, New Delhi",
        estimated_weight=15.0,
        scrap_category=category
    )
    print("Created Pending Request: 456 Pending Lane")

    # 2. My Task (Assigned to Agent)
    PickupRequest.objects.create(
        customer=customer,
        agent=agent,
        status=PickupRequest.Status.ASSIGNED,
        scheduled_date=timezone.now() + timedelta(hours=4),
        address="789 Assigned Road, New Delhi",
        estimated_weight=25.0,
        scrap_category=category
    )
    print("Created My Task: 789 Assigned Road")

    # 3. Completed Task (Collected by Agent)
    PickupRequest.objects.create(
        customer=customer,
        agent=agent,
        status=PickupRequest.Status.COLLECTED,
        scheduled_date=timezone.now() - timedelta(days=2),
        completed_at=timezone.now() - timedelta(days=1),
        address="101 Completed Blvd, New Delhi",
        estimated_weight=50.0,
        actual_weight=48.5,
        total_amount=48.5 * float(category.rate_per_kg),
        scrap_category=category
    )
    print("Created Completed Task: 101 Completed Blvd")
    
    print("\nDashboard Test Data Ready!")

if __name__ == "__main__":
    setup_dashboard_data()

import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from core.models import User, PickupRequest, ScrapCategory, PickupItem
from django.utils import timezone

def test_agent_portal():
    # Setup Data
    agent = User.objects.get(username='agent01')
    customer = User.objects.first() # Any customer
    
    # Ensure categories exist
    paper, _ = ScrapCategory.objects.get_or_create(name='Newspaper', defaults={'rate_per_kg': 14})
    iron, _ = ScrapCategory.objects.get_or_create(name='Iron', defaults={'rate_per_kg': 26})
    
    # Create a Pickup Request
    pickup = PickupRequest.objects.create(
        customer=customer,
        agent=agent,
        status=PickupRequest.Status.ASSIGNED,
        scheduled_date=timezone.now(),
        address='Test Address',
        estimated_weight=10.0
    )
    print(f"Created Test Pickup: {pickup.id}")
    
    # Prepare Post Data
    client = Client()
    client.force_login(agent)
    
    url = f'/agent/job/{pickup.id}/'
    
    # Simulate adding 5kg Newspaper and 2kg Iron
    post_data = {
        'category[]': [paper.id, iron.id],
        'weight[]': ['5.0', '2.0']
    }
    
    print("Submitting collection data...")
    response = client.post(url, post_data)
    
    if response.status_code == 302:
        print("Success: Redirected after POST")
    else:
        print(f"Failed: Status Code {response.status_code}")
        return

    # Verify Results
    pickup.refresh_from_db()
    
    print(f"Status: {pickup.status}")
    print(f"Total Amount: {pickup.total_amount}")
    print(f"Actual Weight: {pickup.actual_weight}")
    
    items = pickup.items.all()
    print(f"Items Created: {items.count()}")
    for item in items:
        print(f"- {item.category.name}: {item.weight}kg = ₹{item.amount}")
        
    expected_amount = (5.0 * float(paper.rate_per_kg)) + (2.0 * float(iron.rate_per_kg))
    if float(pickup.total_amount) == expected_amount:
        print(f"VERIFICATION PASSED: Amount matches expected ₹{expected_amount}")
    else:
        print(f"VERIFICATION FAILED: Expected ₹{expected_amount}, got ₹{pickup.total_amount}")

if __name__ == '__main__':
    test_agent_portal()

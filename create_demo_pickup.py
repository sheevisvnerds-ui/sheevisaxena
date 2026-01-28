import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from core.models import User, PickupRequest

def create_demo_data():
    agent = User.objects.get(username='agent01')
    # Get a customer (create one if not exists)
    customer = User.objects.filter(role=User.Role.CUSTOMER).first()
    if not customer:
        customer = User.objects.create_user('customer01', 'cust@example.com', 'password123', role=User.Role.CUSTOMER, name='Demo Customer')
    
    # Create a fresh ASSIGNED pickup
    pickup = PickupRequest.objects.create(
        customer=customer,
        agent=agent,
        status=PickupRequest.Status.ASSIGNED,
        scheduled_date=timezone.now(),
        address='123 Demo Street, Tech Park',
        estimated_weight=25.0
    )
    print(f"Created Demo Pickup #{pickup.id} for agent {agent.username}")
    print("Refresh your Agent Dashboard to see it.")

if __name__ == '__main__':
    create_demo_data()

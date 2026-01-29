import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from core.models import PickupRequest, PickupStatusUpdate, User

def seed_tracking_data():
    # Get the most recent pickup
    pickup = PickupRequest.objects.last()
    
    if not pickup:
        print("No pickup requests found. Please create a pickup request first.")
        return

    print(f"Adding tracking updates to Pickup #{pickup.id} for {pickup.customer.username}...")

    # Clear existing updates to avoid duplicates if this is run multiple times
    PickupStatusUpdate.objects.filter(pickup=pickup).delete()

    # Add sample updates
    updates = [
        {
            "status": "Order Placed",
            "location": "Online",
            "description": "Pickup request has been received.",
        },
        {
            "status": "Agent Assigned",
            "location": "System",
            "description": "An agent has been assigned to your request.",
        },
        {
            "status": "On the Way",
            "location": "Main Market, City Center",
            "description": "Agent is 2km away.",
        }
    ]

    for data in updates:
        PickupStatusUpdate.objects.create(
            pickup=pickup,
            status=data['status'],
            location=data['location'],
            description=data['description']
        )
        print(f"Added update: {data['status']}")

    print("Done! Refresh the Customer Tracking page to see the timeline.")

if __name__ == '__main__':
    seed_tracking_data()

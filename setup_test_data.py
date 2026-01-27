import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import ScrapCategory, PickupRequest

User = get_user_model()

def setup_data():
    print("Setting up test data...")

    # 1. Create Users
    # Admin
    if not User.objects.filter(username='admin_user').exists():
        User.objects.create_superuser('admin_user', 'admin@example.com', 'testpass123', role=User.Role.ADMIN, name='Super Admin')
        print("Created Admin: admin_user / testpass123")
    else:
        print("Admin user already exists")

    # Customer
    customer, created = User.objects.get_or_create(username='test_customer', defaults={
        'email': 'customer@example.com',
        'is_staff': False,
        'role': User.Role.CUSTOMER,
        'name': 'Rahul Customer',
        'address': '123 Green Park, Delhi'
    })
    if created:
        customer.set_password('testpass123')
        customer.save()
        print("Created Customer: test_customer / testpass123")
    else:
        print("Customer user already exists")

    # Agent
    agent, created = User.objects.get_or_create(username='test_agent', defaults={
        'email': 'agent@example.com',
        'is_staff': False, 
        # Note: In a real app agents might need is_staff=True to access some parts, 
        # but here we have a custom dashboard.
        'role': User.Role.AGENT, 
        'name': 'Suresh Agent',
        'phone': '9876543210'
    })
    if created:
        agent.set_password('testpass123')
        agent.save()
        print("Created Agent: test_agent / testpass123")
    else:
        print("Agent user already exists")

    print("\nTest Data Setup Complete!")
    print("------------------------------------------------")
    print("Login Credentials (Password: testpass123):")
    print("1. Customer: test_customer")
    print("2. Agent:    test_agent")
    print("3. Admin:    admin_user")
    print("------------------------------------------------")

if __name__ == "__main__":
    setup_data()

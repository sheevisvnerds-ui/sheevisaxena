import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from core.models import User

def create_superuser():
    try:
        if not User.objects.filter(username='admin').exists():
            print("Creating superuser 'admin'...")
            User.objects.create_superuser('admin', 'admin@example.com', 'admin', role=User.Role.ADMIN, name='System Admin')
            print("Superuser created successfully.")
        else:
            print("Superuser 'admin' already exists.")
    except Exception as e:
        print(f"Error creating superuser: {e}")

if __name__ == '__main__':
    create_superuser()
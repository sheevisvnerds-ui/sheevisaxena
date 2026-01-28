import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from core.models import User

def create_agent():
    username = 'agent01'
    password = 'password123'
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(
            username=username, 
            password=password, 
            role=User.Role.AGENT, 
            name='Test Agent'
        )
        print(f"Agent user created: {username} / {password}")
    else:
        print(f"Agent user '{username}' already exists. Password: {password}")

if __name__ == '__main__':
    create_agent()

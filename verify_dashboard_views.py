import os
import django
from django.test import Client
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapewale.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import PickupRequest

User = get_user_model()

def verify_dashboard():
    print("Verifying Agent Dashboard Views...")
    c = Client()
    
    # 1. Login
    print("Attempting Login...")
    login_success = c.login(username='test_agent', password='testpass123')
    if not login_success:
        print("FAIL: Login failed for test_agent")
        return
    print("PASS: Login successful")

    # 2. Get Dashboard
    url = reverse('agent_dashboard')
    print(f"Fetching {url}...")
    # Use 127.0.0.1 as host, assuming it is allowed in settings
    response = c.get(url, HTTP_HOST='127.0.0.1')
    
    if response.status_code != 200:
        print(f"FAIL: Dashboard returned status {response.status_code}")
        return
    print("PASS: Dashboard returned 200 OK")

    content = response.content.decode('utf-8')

    # 3. Check Tabs Presence
    tabs = ["My Tasks", "Pending Requests", "Task Completed"]
    for tab in tabs:
        if tab in content:
            print(f"PASS: Found tab '{tab}'")
        else:
            print(f"FAIL: Missing tab '{tab}'")
            
    # 4. Check Activity Data in Context
    # We expect context to have 'my_tasks', 'pending_requests', 'completed_tasks'
    # Based on setup_dashboard_test_data.py, we created 1 of each.
    
    # Note: response.context might only be available if using render() which we are.
    if response.context:
        my_tasks = response.context.get('my_tasks')
        pending = response.context.get('pending_requests')
        completed = response.context.get('completed_tasks')
        
        if len(my_tasks) >= 1:
            print(f"PASS: my_tasks count = {len(my_tasks)}")
        else:
            print(f"FAIL: my_tasks count is {len(my_tasks)}, expected >= 1")

        if len(pending) >= 1:
            print(f"PASS: pending_requests count = {len(pending)}")
        else:
            print(f"FAIL: pending_requests count is {len(pending)}, expected >= 1")

        if len(completed) >= 1:
            print(f"PASS: completed_tasks count = {len(completed)}")
        else:
            print(f"FAIL: completed_tasks count is {len(completed)}, expected >= 1")
    else:
        print("WARN: Could not access response context (maybe TemplateView behavior in test client)")

    # 5. Check Rendered HTML for specific task IDs if context check failed or as double check
    # We created tasks, their IDs might vary but we can check for strings like "456 Pending Lane"
    if "456 Pending Lane" in content:
        print("PASS: Found Pending Task '456 Pending Lane' in HTML")
    else:
        print("FAIL: Did not find '456 Pending Lane'")

    if "789 Assigned Road" in content:
         print("PASS: Found My Task '789 Assigned Road' in HTML")
    else:
        print("FAIL: Did not find '789 Assigned Road'")

    if "101 Completed Blvd" in content:
         print("PASS: Found Completed Task '101 Completed Blvd' in HTML")
    else:
        print("FAIL: Did not find '101 Completed Blvd'")

    print("\nVerification Complete.")

if __name__ == "__main__":
    verify_dashboard()

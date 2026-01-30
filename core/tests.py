from django.test import TestCase, Client
from django.urls import reverse
from core.forms import UnifiedSignupForm

class SignupViewTest(TestCase):
    def test_signup_page_has_role_dropdown(self):
        """Test that the signup page displays a role selection field as a dropdown."""
        client = Client()
        response = client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        
        # Check that 'role' is in the form fields
        form = response.context['form']
        self.assertIn('role', form.fields)
        
        # Ensure it is using the correct form class
        self.assertIsInstance(form, UnifiedSignupForm)
        
        # Check for dropdown behavior in HTML (select tag)
        self.assertContains(response, '<select')
        self.assertContains(response, 'name="role"')
        self.assertContains(response, 'value="CUSTOMER"')
        self.assertContains(response, 'value="AGENT"')

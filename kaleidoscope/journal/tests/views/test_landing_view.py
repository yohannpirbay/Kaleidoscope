from django.test import TestCase, Client
from django.urls import reverse
from journal.models import User
from django.utils import timezone
from datetime import datetime, timedelta

class LandingViewTestCase(TestCase):
    fixtures=["journal/tests/fixtures/default_user.json"]
    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
       

    def test_get_request(self):
        self.client.login(username=self.user.username,password="Password123")
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing.html')
        # Check if the user's last login is updated correctly
        self.user.refresh_from_db()
        self.assertEqual(timezone.localtime(self.user.last_login).date(), timezone.now().date())
        
    def test_post_request(self):
        response = self.client.post(reverse('landing'))
        self.assertEqual(response.status_code, 302)  # Method not allowed

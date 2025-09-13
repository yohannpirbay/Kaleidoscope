from django.test import TestCase, Client
from django.urls import reverse
from journal.models import Reminder, User
from journal.forms import ReminderForm

class ReminderViewTest(TestCase):
    """Tests for the user reminders view."""

    fixtures = ['journal/tests/fixtures/default_user.json']
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username='@johndoe')

    def test_get_request(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('achievements'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ReminderForm)
        self.assertTemplateUsed(response, 'achievements.html')

    def test_post_request_valid_form(self):
        self.client.force_login(self.user)
        form_data = {'name': 'Test Reminder', 'description': 'Test Description', 'value': 10} 
        response = self.client.post(reverse('achievements'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/achievements/")


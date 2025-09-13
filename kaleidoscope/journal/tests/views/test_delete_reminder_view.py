from django.test import TestCase, Client
from django.urls import reverse
from journal.models import Reminder, User
import json

class DeleteReminderViewTest(TestCase):
    """Tests for the deletion of a reminder view."""

    fixtures=["journal/tests/fixtures/default_user.json"]
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username="@johndoe")
        self.client.force_login(self.user)
        self.reminder = Reminder.objects.create(user=self.user, name='Test Reminder', description='Test Description', value=5)

    def test_delete_reminder_success(self):
        initial_count = Reminder.objects.count()
        response = self.client.post(reverse('delete_reminder'), data=json.dumps({'id': self.reminder.id}), content_type='application/json')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(json.loads(response.content)['success'])
        self.assertEqual(Reminder.objects.count(), initial_count - 1)
    
    def test_delete_reminder_invalid_id(self):
        response = self.client.post(reverse('delete_reminder'), data=json.dumps({'id': 999}), content_type='application/json')
        self.assertEqual(response.status_code,404)
        self.assertEqual(response.json()['error'],"Reminder not found")

    def test_delete_reminder_invalid_method(self):
        initial_count = Reminder.objects.count()
        response = self.client.get(reverse('delete_reminder'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Reminder.objects.count(), initial_count) 

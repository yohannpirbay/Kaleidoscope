from django.test import TestCase, Client
from django.urls import reverse
from journal.models import Entry, User
from datetime import datetime
import pytz

class ArchivesViewTest(TestCase):
    """Tests for the entry archives view."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_login(self.user)
        self.entry1 = Entry.objects.create(user=self.user, title="Test Title 1", text='Test entry 1', mood=5, date_created=datetime.now(tz=pytz.timezone('Europe/London')))
        self.entry2 = Entry.objects.create(user=self.user,title="Test Title 2", text='Test entry 2', mood=1, date_created=datetime.now(tz=pytz.timezone('Europe/London')))
        self.entry3 = Entry.objects.create(user=self.user, title="Test Title 3", text='Test entry 3', mood=3, date_created=datetime.now(tz=pytz.timezone('Europe/London')))

    def test_get_request(self):
        response = self.client.get(reverse('archives'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'archives.html')
        self.assertTrue('months' in response.context)

    def test_archives_months(self):
        response = self.client.get(reverse('archives'))
        months = response.context['months']
        self.assertEqual(len(months), 1) 
        self.assertIn(f"{datetime.now().date().strftime('%B')} {datetime.now().date().year}" , months)

    def test_archives_entries(self):
        response = self.client.get(reverse('archives'))
        months = response.context['months']
        self.assertEqual(len(months[f"{datetime.now().date().strftime('%B')} {datetime.now().date().year}"]), 3) 

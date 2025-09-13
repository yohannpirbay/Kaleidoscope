"""Testing the dashboard in the views"""
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from journal.models import User, Entry
import json

class DashboardViewTest(TestCase):
    """Tests for the journal dashboard view."""

    def setUp(self):
        self.user1 = User.objects.create_user(username='@user1', email='user1@email.com', password='Password123')
        self.user2 = User.objects.create_user(username='@user2', email='user2@email.com', password='Password123')

        Entry.objects.create(user=self.user1, text='User 1 Entry 1', date_created=timezone.now())
        Entry.objects.create(user=self.user1, text='User 1 Entry 2', date_created=timezone.now())
        Entry.objects.create(user=self.user2, text='User 2 Entry 1', date_created=timezone.now())

        self.client = Client()

    # Test when access to a dashboard is unauthenticated
    def test_dashboard_access_unauthenticated(self):
        response = self.client.get(reverse('dashboard'))
        self.assertNotEqual(response.status_code, 200)

    # Test user1 has the correct dashboard entires
    def test_dashboard_for_user1(self):
        self.client.login(username='@user1', password='Password123')

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        entries = [entry for entry in response.context['entries'] if not entry.is_template]
        self.assertEqual(len(entries), 2)
        for entry in entries:
            self.assertEqual(entry.user, self.user1)

    # Test user2 has the correct dashboard entries
    def test_dashboard_for_user2(self):
        self.client.login(username='@user2', password='Password123')

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

        entries = [entry for entry in response.context['entries'] if not entry.is_template]
        self.assertEqual(len(entries), 1)
        for entry in entries:
            self.assertEqual(entry.user, self.user2)

    def test_create_entry(self):
        self.client.login(username='@user1', password='Password123')
        response = self.client.post(reverse('create_entry'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,"/dashboard/")

    def test_get_entry(self):
        entry = Entry.objects.create(user=self.user1, text='Test Entry', date_created=timezone.now())
        self.client.login(username='@user1', password='Password123')  # Ensure user is logged in
        response = self.client.get(reverse('get_entry', kwargs={'entry_id': entry.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['text'], 'Test Entry')
    
    def test_update_entry(self):
        self.client.login(username='@user1', password='Password123')
        entry = Entry.objects.create(user=self.user1, text='Old Entry', date_created=timezone.now())
        
        updated_text = 'Updated Entry'
        updated_title = "Updated Title"
        response = self.client.post(reverse('update_entry', kwargs={'entry_id': entry.id}), data=json.dumps({'title':updated_title, 'text': updated_text}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        
        entry.refresh_from_db()
        self.assertEqual(entry.text, updated_text)
    
    def test_delete_entry(self):
        self.client.login(username='@user1', password='Password123')
        entry = Entry.objects.create(user=self.user1, text='Entry to delete', date_created=timezone.now())
        
        response = self.client.delete(reverse('delete_entry', kwargs={'entry_id': entry.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

        # Check that the entry has been deleted
        with self.assertRaises(Entry.DoesNotExist):
            Entry.objects.get(id=entry.id)
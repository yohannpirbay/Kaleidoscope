from django.test import TestCase
from django.urls import reverse
from journal.models import Entry, User
from journal.tests.helpers import reverse_with_next
import json

class EntryViewTestCase(TestCase):
    """Tests for the journal's entry view."""

    fixtures = ['journal/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.entry = Entry.objects.create(user=self.user,title="Test Title",  mood=0,text="Test Entry")
    
    def test_create_entry_post_logged_out(self):
        response = self.client.post(reverse('create_entry'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)

    def test_create_entry_get_logged_out(self):
        response = self.client.get(reverse('create_entry'))        
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)
    
    def test_create_entry_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(reverse('create_entry'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Entry.objects.filter(user=self.user, text="Test Entry").exists())
        self.assertTemplateUsed("dashboard.html")
    
    def test_create_entry_get_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(reverse('create_entry'))
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(response.json()['status'], 'error')

    def test_get_entry_logged_out(self):
        response = self.client.get(reverse('get_entry', kwargs={'entry_id': self.entry.id}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)

    def test_get_entry_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(reverse('get_entry', kwargs={'entry_id': self.entry.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['text'], "Test Entry")
    
    def test_get_entry_invalid_entry(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.put(reverse('get_entry', kwargs={'entry_id': 999}))
        self.assertEqual(response.json()["status"],"error")

    def test_update_entry_logged_out(self):
        data = {'text': 'Updated Entry'}
        response = self.client.put(reverse('update_entry', kwargs={'entry_id': self.entry.id}), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)

    def test_update_entry_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        data = {'title':"Updated Title", 'mood':3,'text': 'Updated Entry'}
        response = self.client.put(reverse('update_entry', kwargs={'entry_id': self.entry.id}), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        updated_entry = Entry.objects.get(id=self.entry.id)
        self.assertEqual(updated_entry.text, 'Updated Entry')
        self.assertEqual(response.json()['status'], 'success')
    
    def test_update_entry_invalid_entry(self):
        self.client.login(username=self.user.username, password="Password123")
        data = {'title':"Updated Title",'mood':1,'text': 'Updated Entry'}
        response = self.client.put(reverse('update_entry', kwargs={'entry_id': 999}), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.json()["status"],"error")

    def test_delete_entry_logged_out(self):
        response = self.client.delete(reverse('delete_entry', kwargs={'entry_id': self.entry.id}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)

    def test_delete_entry_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.delete(reverse('delete_entry', kwargs={'entry_id': self.entry.id}))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Entry.objects.filter(id=self.entry.id).exists())
        self.assertEqual(response.json()['status'], 'success')
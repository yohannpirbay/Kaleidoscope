from django.test import TestCase
from django.urls import reverse
from journal.models import Entry, User


class EntryFromTemplateTestCase(TestCase):
    """Tests for the entry creation from templates."""

    fixtures = ['journal/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.template = Entry.objects.create(user=self.user,title="Test Title", text="Test Entry", is_template=True)
    
    def test_create_entry_from_template_logged_out(self):
        response = self.client.post(reverse('create_entry_from_template'), {'template_id': self.template.id})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)
        
    def test_create_entry_from_template_logged_in(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(reverse('create_entry_from_template'), {'template_id': self.template.id})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Entry.objects.filter(is_template=False).count(), 1)
        new_entry = Entry.objects.get(is_template=False)
        self.assertEqual(new_entry.title, self.template.title)
        self.assertEqual(new_entry.text, self.template.text)
    
    def test_create_entry_from_template_no_template_id(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(reverse('create_entry_from_template'))
        self.assertEqual(response.status_code, 400)
        self.assertIn('No template selected', response.content.decode())
    
    def test_create_entry_from_template_invalid_method(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(reverse('create_entry_from_template'))
        self.assertEqual(response.status_code, 405)
        self.assertIn('Invalid request', response.content.decode())


    
    
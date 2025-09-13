from django.test import TestCase
from django.urls import reverse
from journal.models import Entry, User

class UpdateTemplateTestCase(TestCase):
    """Tests for updating templates."""

    fixtures = ['journal/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.template = Entry.objects.create(user=self.user,title="Test Title", text="Test Entry", is_template=True)
    
    def test_update_template_logged_out(self):
        response = self.client.post(reverse('create_entry_from_template'), {'template_id': self.template.id})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)
    
    def test_update_template_success(self):
        self.client.login(username=self.user.username, password="Password123")
        new_data = {
            'template_title': 'New Title',
            'template_id': self.template.id,
            'template_text': 'New text',
        }
        response = self.client.post(reverse('update_template'), new_data)
        self.assertRedirects(response, reverse('templates'))
        updated_template = Entry.objects.get(id=self.template.id)
        self.assertEqual(updated_template.title, 'New Title')
        self.assertEqual(updated_template.text, 'New text')
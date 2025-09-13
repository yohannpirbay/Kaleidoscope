from django.test import TestCase
from django.urls import reverse
from journal.models import Entry, User


class DeleteTemplateViewTestCase(TestCase):
    """Tests for the template deletion."""

    fixtures = ['journal/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.template = Entry.objects.create(user=self.user,title="Test Title", text="Test Entry", is_template=True)
    
    def test_delete_template_logged_out(self):
        response = self.client.post(reverse('delete_template', args=[self.template.id]))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)

    def test_delete_template(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(reverse('delete_template', args=[self.template.id]))        
        self.assertRedirects(response, reverse('templates'))
        self.assertFalse(Entry.objects.filter(id=self.template.id).exists())
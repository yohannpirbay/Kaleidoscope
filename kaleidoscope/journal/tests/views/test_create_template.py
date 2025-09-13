from django.test import TestCase
from django.urls import reverse
from journal.models import Entry, User


class CreateTemplateTestCase(TestCase):
    """Tests for the template creation."""

    fixtures = ['journal/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
    
    def test_create_template_logged_out(self):
        new_template_data = {
            'template_title': 'Test Template',
            'template_text': 'This is a test template.',
        }
        response = self.client.post(reverse('create_template'), new_template_data)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)

    def test_create_template(self):
        self.client.login(username=self.user.username, password="Password123")
        new_template_data = {
            'template_title': 'Test Template',
            'template_text': 'This is a test template.',
        }
        response = self.client.post(reverse('create_template'), new_template_data)
        self.assertRedirects(response, reverse('templates'))
        self.assertTrue(Entry.objects.filter(user=self.user, is_template=True, title='Test Template').exists())
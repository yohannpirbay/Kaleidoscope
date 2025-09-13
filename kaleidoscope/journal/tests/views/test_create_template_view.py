from django.test import TestCase
from django.urls import reverse
from journal.models import Entry, User


class CreateTemplateViewTestCase(TestCase):
    """Tests for the template creation."""

    fixtures = ['journal/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
    
    def test_create_template_logged_out(self):
        response = self.client.post(reverse('create_a_new_template'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)

    def test_create_template_post(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(reverse('create_a_new_template'))        
        self.assertRedirects(response, reverse('templates'))
    
    def test_create_template_get(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(reverse('create_a_new_template'))        
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'new_template.html') 

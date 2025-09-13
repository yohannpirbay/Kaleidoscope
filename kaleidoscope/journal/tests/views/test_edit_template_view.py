from django.test import TestCase
from django.urls import reverse
from journal.models import Entry, User


class DeleteTemplateViewTestCase(TestCase):
    """Tests for template editing."""

    fixtures = ['journal/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.template = Entry.objects.create(user=self.user,title="Original Title", text="Original text", is_template=True)

    def test_edit_template_post_logged_out(self):
        response = self.client.post(reverse('edit_template', kwargs={'template_id': self.template.id}))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/log_in/', response.url)

    def test_edit_template_post(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.post(reverse('edit_template', kwargs={'template_id': self.template.id}))
        self.assertRedirects(response, '/templates/')
    
    def test_edit_template_get(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(reverse('edit_template', kwargs={'template_id': self.template.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_template.html')
        self.assertEqual(response.context['template_id'], self.template.id)
        self.assertEqual(response.context['template_text'], "Original text")
        self.assertEqual(response.context['template_title'], "Original Title")
        


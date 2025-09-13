from django.test import TestCase
from django.urls import reverse
from journal.models import User,Entry
import json

class SingleDownloadViewTestCase(TestCase):
    fixtures = ['journal/tests/fixtures/default_user.json', 'journal/tests/fixtures/default_entry.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.entry = Entry.objects.get(pk=1)

    def test_post_request(self):
        self.client.force_login(self.user)
        url = reverse('single_download')
        response = self.client.post(url, data={"entryTitle":self.entry.title,"entryText":self.entry.text}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_post_request_invalid_json(self):
        self.client.force_login(self.user)
        url = reverse('single_download')
        response = self.client.post(url, data='invalid_json', content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_unauthenticated(self):
        url = reverse('single_download')
        response = self.client.post(url, data={"entryTitle":self.entry.title,"entryText":self.entry.text}, content_type='application/json')
        self.assertEqual(response.status_code, 302)

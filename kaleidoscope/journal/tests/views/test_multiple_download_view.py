from django.test import TestCase
from django.urls import reverse
from journal.models import User,Entry
import json
import zipfile
from io import BytesIO

class MultipleDownloadsViewTestCase(TestCase):
    fixtures = ['journal/tests/fixtures/default_user.json', 'journal/tests/fixtures/default_entry.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.entries = Entry.objects.filter(pk=1)

    def test_post_request(self):
        entry_ids = [str(entry.id) for entry in self.entries]
        json_data = {'entries': entry_ids}
        self.client.force_login(self.user)
        url = reverse('multiple_download')
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/zip')
        # Check if all entries are included in the zip file
        with zipfile.ZipFile(BytesIO(response.content), 'r') as zip_file:
            for entry in self.entries:
                self.assertIn(f'{entry.title}.pdf', zip_file.namelist())

    def test_post_request_invalid_json(self):
        self.client.force_login(self.user)
        url = reverse('multiple_download')
        response = self.client.post(url, data='invalid_json', content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_request_unauthenticated(self):
        url = reverse('multiple_download')
        response = self.client.post(url, data={}, content_type='application/json')
        self.assertEqual(response.status_code, 302)
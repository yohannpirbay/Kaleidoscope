from django.test import TestCase, Client
from django.urls import reverse
from journal.models import Entry, User

class ToggleBookmarViewTest(TestCase):
    
    fixtures=["journal/tests/fixtures/default_entry.json","journal/tests/fixtures/default_user.json"]
    def setUp(self):
        self.user = User.objects.get(username="@johndoe")
        self.entry = Entry.objects.get(pk=1)

    def test_toggle_bookmark_authenticated(self):
        self.client.login(username=self.user.username, password="Password123")
        url = reverse('toggle_bookmark', args=[self.entry.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.entry.refresh_from_db()
        self.assertTrue(self.entry.bookmarked)

    def test_toggle_bookmark_unauthenticated(self):
        url = reverse('toggle_bookmark', args=[self.entry.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  
        self.entry.refresh_from_db()
        self.assertFalse(self.entry.bookmarked)

    def test_toggle_bookmark_invalid_entry(self):
        self.client.login(username=self.user.username, password="Password123")
        url = reverse('toggle_bookmark', args=[999])
        response = self.client.post(url)
        self.assertEqual(response.json()["status"], "error")
        
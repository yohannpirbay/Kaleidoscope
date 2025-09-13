from django.test import TestCase, Client
from django.urls import reverse
from journal.models import Reminder, Achievement, Entry,User
from datetime import datetime, timezone,timedelta
class AchievementViewTest(TestCase):
    """Tests for achievements view."""

    fixtures = ['journal/tests/fixtures/default_user.json']
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username="@johndoe")
        self.reminder = Reminder.objects.create(user=self.user, name='Test Reminder', description='Test Description', value=0)
        self.achievement1 = Achievement.objects.create(name='Test Achievement', description='Test Description', value=10)
        self.achievement2 = Achievement.objects.create(name='Test Achievement 2', description='Test Description 2', value=2)
        self.user.achievements.add(self.achievement1)
        self.user.achievements.add(self.achievement2)
        self.entry = Entry.objects.create(user=self.user, text='Test entry', mood=4,date_created=datetime(2024,1,3,tzinfo=None))
        self.entry2 = Entry.objects.create(user=self.user, text='Another test entry', mood=1,date_created =datetime(2024,1,4,tzinfo=None))
        self.entry3 = Entry.objects.create(user=self.user, text='Test entry 2', mood=5,date_created=datetime.now())
        self.entry4 = Entry.objects.create(user=self.user, text='Another test entry 2', mood=2.5,date_created =datetime.now()+ timedelta(days=1))
        self.entry5 = Entry.objects.create(user=self.user, text='Another test entry 3', mood=2.9,date_created =datetime.now()+ timedelta(days=2))

    def test_get_request(self):
        self.client.force_login(self.user)
        self.user.last_login=datetime.now() - timedelta(days=2)
        response = self.client.get(reverse('achievements'))
        
        self.achievement1.refresh_from_db()
        self.achievement2.refresh_from_db()

        self.achievement1.update_is_achieved()
        self.achievement2.update_is_achieved()
        self.assertNotEqual(0,self.achievement1.completed)
        self.assertNotEqual(0,self.achievement1.value)
        self.assertNotEqual(0,self.achievement1.percentage_completed)
        self.assertFalse(self.achievement1.is_achieved)
        self.assertTrue(self.achievement2.is_achieved)
        self.assertGreater(self.achievement2.percentage_completed,100)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'achievements.html')
        self.assertTrue('form' in response.context)
        self.assertTrue('reminders' in response.context)
        self.assertTrue('entries' in response.context)
        self.assertTrue('moods' in response.context)
        self.assertTrue('year_dates' in response.context)
        self.assertTrue('word_count' in response.context)
        self.assertTrue('current_streak' in response.context)
        self.assertTrue('longest_streak' in response.context)
        self.assertTrue('achievements' in response.context)
        self.assertTrue('isDaily' in response.context)

    def test_post_request_valid_form(self):
        self.client.force_login(self.user)
        form_data = {'name': 'Test Reminder 2', 'description': 'Test Description 2', 'value': 5}
        response = self.client.post(reverse('achievements'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Reminder.objects.filter(user=self.user, name='Test Reminder 2').exists())

    def test_post_request_invalid_form(self):
        self.client.force_login(self.user)
        form_data = {}
        response = self.client.post(reverse('achievements'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Reminder.objects.filter(user=self.user, name='Test Reminder 2').exists())

    def test_last_login_update(self):
        self.client.force_login(self.user)
        last_login = self.user.last_login
        self.client.get(reverse('achievements'))
        self.user.refresh_from_db()
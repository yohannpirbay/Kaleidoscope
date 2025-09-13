from django.test import TestCase, Client
from django.urls import reverse
from journal.models import Entry, Achievement,User, Reminder
from datetime import datetime,timedelta

class JSTestViewsTestCase(TestCase):
    fixtures=["journal/tests/fixtures/default_user.json"]
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username="@johndoe")
        # self.reminder = Reminder.objects.create(user=self.user, name='Test Reminder', description='Test Description', value=0)
        self.achievement1 = Achievement.objects.create(name='Test Achievement', description='Test Description', value=10)
        self.achievement2 = Achievement.objects.create(name='Test Achievement 2', description='Test Description 2', value=2)
        self.user.achievements.add(self.achievement1)
        self.user.achievements.add(self.achievement2)
        self.entry = Entry.objects.create(user=self.user, text='Test entry', mood=4,date_created=datetime(2024,1,3,tzinfo=None))
        self.entry2 = Entry.objects.create(user=self.user, text='Another test entry', mood=1,date_created =datetime(2024,1,4,tzinfo=None))
        self.entry3 = Entry.objects.create(user=self.user, text='Test entry 2', mood=5,date_created=datetime.now())
        self.entry4 = Entry.objects.create(user=self.user, text='Another test entry 2', mood=2.5,date_created =datetime.now()+ timedelta(days=1))
        self.entry5 = Entry.objects.create(user=self.user, text='Another test entry 3', mood=2.9,date_created =datetime.now()+ timedelta(days=2))
        self.client.force_login(self.user)

    def test_help_button_test(self):
        response = self.client.get(reverse('help_button_test'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tests/help_button_tests.html')

    def test_daily_popup_test(self):
        response = self.client.get(reverse('daily_popup_test'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tests/daily_popup_tests.html')

    def test_sidebar_test(self):
        response = self.client.get(reverse('sidebar_test'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tests/sidebar_tests.html')

    def test_chart_test(self):
        response = self.client.get(reverse('chart_test'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tests/charts_tests.html')

    def test_css_test(self):
        response = self.client.get(reverse('css_test'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tests/css_switch_tests.html')

    def test_journal_test(self):
        response = self.client.get(reverse('journal_test'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tests/journal_tests.html')
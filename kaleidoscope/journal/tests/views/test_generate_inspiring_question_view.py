from django.test import TestCase, Client
from django.urls import reverse
from journal.models import User
import json

class GenerateInspiringQuestionTestCase(TestCase):
    fixtures=["journal/tests/fixtures/default_user.json"]
    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(username="@johndoe")
        self.client.force_login(self.user)

    def test_generate_inspiring_question_post(self):
        #will pass when access to openai api key is present
        data = {'user_input': 'Your user input here'}
        response = self.client.post(reverse('generate_inspiring_question'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        json_response = response.json()
        self.assertIn('status', json_response)

    def test_generate_inspiring_question_get(self):
        response = self.client.get(reverse('generate_inspiring_question'))
        self.assertEqual(response.status_code, 405)

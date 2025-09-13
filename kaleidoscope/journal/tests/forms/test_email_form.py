from django.test import SimpleTestCase
from journal.forms import EmailForm

class EmailFormTestCase(SimpleTestCase):
    """Unit tests of the email form."""

    def test_valid_form(self):
        form_data = {
            'subject': 'Test subject',
            'message': 'Test message',
            'recipient': 'test@example.com',
        }
        form = EmailForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_data(self):
        form = EmailForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['subject'], ['This field is required.'])
        self.assertEqual(form.errors['message'], ['This field is required.'])
        self.assertEqual(form.errors['recipient'], ['This field is required.'])

    def test_invalid_email(self):
        form_data = {
            'subject': 'Test subject',
            'message': 'Test message',
            'recipient': 'invalid_email',
        }
        form = EmailForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['recipient'], ['Enter a valid email address.'])

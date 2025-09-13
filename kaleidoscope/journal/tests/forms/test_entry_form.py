from django.test import TestCase
from journal.forms import EntryForm

class EntryInFormTestCase(TestCase):
    """Unit tests of the entry form."""

    def test_form_contains_required_fields(self):
        """test that the form contains the required fields"""
        form = EntryForm()
        self.assertIn('text', form.fields)

    def test_valid_form(self):
        """test that the form is deemed valid when submitted with valid data"""
        form_data = {'text': 'This is a test entry.'}
        form = EntryForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form(self):
        """test that the form is deemed invalid when submitted empty"""
        form_data = {'text': ''}
        form = EntryForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('text' in form.errors)
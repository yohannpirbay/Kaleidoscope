"""Unit tests for the Entry model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from journal.models import Entry

class EntryModelTestCase(TestCase):
    """Unit tests for the Entry model."""

    fixtures = [
        'journal/tests/fixtures/default_entry.json',
        'journal/tests/fixtures/default_user.json'
        ]

    def setUp(self):
        self.entry = Entry.objects.get(pk=1)
    
    def test_entry_creation(self):
        """test that the fixture we have is created successfuly"""
        self._assert_entry_is_valid()
    
    def test_text_cannot_be_blank(self):
        """test that an entry with blank text is deemed invalid"""
        self.entry.text = ''
        self._assert_entry_is_invalid()
    
    def _assert_entry_is_valid(self):
        try:
            self.entry.full_clean()
        except (ValidationError):
            self.fail('Test entry should be valid')

    def _assert_entry_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.entry.full_clean()
        
    def test_title(self):
        self.assertEqual(self.entry.title, "Default Title")
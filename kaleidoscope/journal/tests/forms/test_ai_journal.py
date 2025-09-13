from django.test import SimpleTestCase
from unittest.mock import patch
from journal.ai_journal import generate_ai_question, remove_quotes, clean_response

class AIJournalSubFunctionsTest(SimpleTestCase):
    def test_remove_quotes_with_quotes(self):
        """Test remove_quotes function with a string that has leading and trailing quotes."""
        input_str = '"This is a test string"'
        expected_result = 'This is a test string'
        # Call the function directly if accessible
        result = remove_quotes(input_str)
        self.assertEqual(result, expected_result)

    def test_remove_quotes_without_quotes(self):
        """Test remove_quotes function with a string without leading and trailing quotes."""
        input_str = 'This is a test string'
        expected_result = 'This is a test string'
        # Call the function directly if accessible
        result = remove_quotes(input_str)
        self.assertEqual(result, expected_result)

    def test_clean_response_with_unwanted_substring(self):
        """Test clean_response function with a text ending with an unwanted substring."""
        input_str = 'This is a test string.'
        unwanted_substring = '.'
        expected_result = 'This is a test string'
        result = clean_response(input_str, unwanted_substring)
        self.assertEqual(result, expected_result)

    def test_clean_response_without_unwanted_substring(self):
        """Test clean_response function with a text not ending with an unwanted substring."""
        input_str = 'This is a test string'
        unwanted_substring = '.'
        expected_result = 'This is a test string'
        result = clean_response(input_str, unwanted_substring)
        self.assertEqual(result, expected_result)

class GenerateAIQuestionAPITest(SimpleTestCase):
    @patch('journal.ai_journal.openai.Completion.create')
    def test_generate_ai_question_prompt(self, mock_create):
        """Test generate_ai_question prompt is appended with user input correctly."""
        user_input = "Went for a walk in the park."
        expected_start_of_prompt = "You are JournalGPT, a helpful, kind and caring AI that helps journalling users find inspiration."
        expected_end_of_prompt = f"\n\nInput: \"{user_input}\"\nOutput:"

        generate_ai_question(user_input)

        args, kwargs = mock_create.call_args
        actual_prompt = kwargs['prompt']

        self.assertTrue(actual_prompt.startswith(expected_start_of_prompt))
        self.assertTrue(actual_prompt.endswith(expected_end_of_prompt))

        self.assertEqual(kwargs['engine'], 'journaltemplater')
        self.assertEqual(kwargs['temperature'], 0.85)


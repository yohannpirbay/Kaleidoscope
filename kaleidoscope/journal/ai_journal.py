import os
import openai

openai.api_type = "azure"
openai.api_base = "https://journaltemplates.openai.azure.com/"
openai.api_version = "2023-09-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_ai_question(user_input):
    """
    Generates a question that encourages deep thought and emotional exploration based on the user's input.

        Args:
            user_input (str): The user's input representing what they have done today.

        Returns:
            str: A question that aims to help users identify emotions, recall their experience through the senses, and find potential revelations revealed by what they did today.
    """
    
    prompt_template = (
        "You are JournalGPT, a helpful, kind and caring AI that helps journalling users find inspiration. You do this acting like a function, your input is what the user has done today, and your output will be a question that encourages deep thought and emotional exploration. Your question should aim to help users identify emotions that arose, recall their experience through the senses and find potential revelations revealed by what they did today. \n\nInput: \"{user_input}\"\nOutput:"
    )

    prompt = prompt_template.format(user_input=user_input)

    response = openai.Completion.create(
        engine="journaltemplater",
        prompt=prompt,
        temperature=0.85,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )

    unwanted_substring = "<|im_end|>" 
    cleaned_text = clean_response(response.choices[0].text, unwanted_substring)
    cleaned_text = remove_quotes(cleaned_text)
    return cleaned_text

def remove_quotes(text):
    """
    Removes quotes from the given text if it is enclosed in quotes.

        Args:
            text (str): The text that may or may not be enclosed in quotes.

        Returns:
            str: The text with quotes removed if it was enclosed in quotes, otherwise the original text.
    """

    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    return text

def clean_response(text, unwanted_substring):
    """
    Cleans the response text by removing the unwanted substring from the end of the text.

        Args:
            text (str): The text to be cleaned.
            unwanted_substring (str): The substring to be removed from the end of the text.

        Returns:
            str: The cleaned text with the unwanted substring removed from the end.
    """

    if text.endswith(unwanted_substring):
        return text[:-len(unwanted_substring)].strip()
    return text.strip()
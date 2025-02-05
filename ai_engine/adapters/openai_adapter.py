# ai-test-generator/ai_engine/adapters/openai_adapter.py

import os
from openai import OpenAI
from ai_engine.adapters.base_adapter import BaseAdapter

class OpenAIAdapter(BaseAdapter):
    """
    Adapter for integrating with OpenAI's GPT-based models using the new API format.
    """

    def __init__(self, api_key: str = None, model: str = "gpt-4-turbo"):
        """
        :param api_key: API key for OpenAI.
        :param model: The model to use (default: gpt-3.5-turbo).
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not provided.")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)

    def complete(self, prompt: str, **kwargs) -> str:
        """
        Sends a prompt to the OpenAI API and returns the generated text.
        
        :param prompt: The prompt to be completed.
        :param kwargs: Additional parameters for the API call (temperature, max_tokens, etc.)
        :return: The generated completion as a string.
        """
        # Prepare request parameters for the chat completion API
        params = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1500),
            "n": kwargs.get("n", 1)
        }
        
        # Use the new API format
        response = self.client.chat.completions.create(**params)
        
        # Extract and return the content from the first response choice
        generated_text = response.choices[0].message.content.strip()
        return generated_text

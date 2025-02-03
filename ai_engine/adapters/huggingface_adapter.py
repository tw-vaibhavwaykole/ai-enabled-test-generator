# ai-test-generator/ai_engine/adapters/huggingface_adapter.py

import os
from transformers import pipeline
from ai_engine.adapters.base_adapter import BaseAdapter

class HuggingFaceAdapter(BaseAdapter):
    """
    Adapter for integrating with Hugging Face's text generation pipelines.
    """
    def __init__(self, model: str = "gpt2", device: int = -1, **kwargs):
        """
        :param model: Hugging Face model identifier.
        :param device: Device to run the model on (-1 for CPU, 0 for GPU).
        """
        self.model_name = model
        self.device = device
        self.generator = pipeline("text-generation", model=self.model_name, device=self.device, **kwargs)

    def complete(self, prompt: str, **kwargs) -> str:
        """
        Generates text completion using the Hugging Face pipeline.
        
        :param prompt: The input prompt for text generation.
        :param kwargs: Additional generation parameters (e.g., max_length, temperature).
        :return: Generated text as a string.
        """
        # Default parameters for text generation
        params = {
            "max_length": kwargs.get("max_length", 150),
            "num_return_sequences": kwargs.get("num_return_sequences", 1),
            "temperature": kwargs.get("temperature", 0.7),
            "do_sample": kwargs.get("do_sample", True)
        }
        results = self.generator(prompt, **params)
        # Extract and return the generated text from the first result.
        generated_text = results[0]["generated_text"]
        return generated_text

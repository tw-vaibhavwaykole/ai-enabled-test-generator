# ai-test-generator/ai_engine/generators/base_generator.py

from abc import ABC, abstractmethod

class BaseGenerator(ABC):
    """
    Abstract base class for test generators.
    This class defines the contract for generating test cases from a unified specification.
    """

    def __init__(self, adapter, prompt_template: str):
        """
        :param adapter: An instance of an AI adapter that implements the complete() method.
        :param prompt_template: A template string for generating the prompt.
        """
        self.adapter = adapter
        self.prompt_template = prompt_template

    @abstractmethod
    def generate(self, unified_spec: dict, **kwargs):
        """
        Generate test cases based on the given specification.
        
        :param unified_spec: A unified specification represented as a dictionary.
        :param kwargs: Additional parameters for test generation.
        :return: A structured test suite or list of test cases.
        """
        pass

    def _compose_prompt(self, unified_spec: dict) -> str:
        """
        Compose the prompt by formatting the template with the given specification.
        
        :param unified_spec: A unified specification as a dictionary.
        :return: A formatted prompt string.
        """
        # For simplicity, we're using Python's format method.
        # In a more advanced scenario, you might integrate a templating engine.
        return self.prompt_template.format(spec=unified_spec)

# ai-test-generator/ai_engine/adapters/base_adapter.py

from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    """
    Abstract Base Adapter for AI provider integrations.
    This interface defines the contract for all adapters.
    """

    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> str:
        """
        Sends a prompt to the AI provider and returns the generated completion.
        
        :param prompt: The prompt text to send.
        :param kwargs: Additional provider-specific parameters.
        :return: The generated response as a string.
        """
        pass

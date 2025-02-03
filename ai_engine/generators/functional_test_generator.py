# ai-test-generator/ai_engine/generators/functional_test_generator.py

from ai_engine.generators.base_generator import BaseGenerator

class FunctionalTestGenerator(BaseGenerator):
    """
    Generator for creating functional test cases based on a unified specification.
    """

    def __init__(self, adapter, prompt_template: str = None):
        prompt_template = prompt_template or "Generate functional tests for the following spec: {spec}"
        super().__init__(adapter, prompt_template)

    def generate(self, unified_spec: dict, **kwargs):
        """
        Generate functional test cases.
        
        :param unified_spec: A unified specification represented as a dictionary.
        :param kwargs: Additional parameters for test generation.
        :return: A dictionary representing the functional test suite.
        """
        prompt = self._compose_prompt(unified_spec)
        # Use the adapter to generate test cases from the composed prompt.
        response = self.adapter.complete(prompt, **kwargs)
        # In a full implementation, parse the response into structured test cases.
        return {
            "type": "functional",
            "spec_summary": unified_spec,
            "generated_tests": response
        }

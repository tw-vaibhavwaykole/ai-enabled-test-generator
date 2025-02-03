# ai-test-generator/ai_engine/generators/security_test_generator.py

from ai_engine.generators.base_generator import BaseGenerator

class SecurityTestGenerator(BaseGenerator):
    """
    Generator for creating security test cases based on a unified specification.
    """

    def __init__(self, adapter, prompt_template: str = None):
        prompt_template = prompt_template or "Generate security tests for the following spec: {spec}"
        super().__init__(adapter, prompt_template)

    def generate(self, unified_spec: dict, **kwargs):
        """
        Generate security test cases.
        
        :param unified_spec: A unified specification represented as a dictionary.
        :param kwargs: Additional parameters for test generation.
        :return: A dictionary representing the security test suite.
        """
        prompt = self._compose_prompt(unified_spec)
        response = self.adapter.complete(prompt, **kwargs)
        return {
            "type": "security",
            "spec_summary": unified_spec,
            "generated_tests": response
        }

# ai-test-generator/ai_engine/orchestrator.py

import logging

# Import generator classes
from ai_engine.generators.functional_test_generator import FunctionalTestGenerator
from ai_engine.generators.security_test_generator import SecurityTestGenerator
from ai_engine.generators.performance_test_generator import PerformanceTestGenerator
from ai_engine.generators.e2e_test_generator import E2ETestGenerator

# Import post-processing functions
from ai_engine.post_processor.syntax_checker import check_syntax
from ai_engine.post_processor.spec_compliance import check_spec_compliance
from ai_engine.post_processor.security_scanner import scan_security

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Orchestrator:
    """
    Coordinates the entire test generation workflow:
      1. Generates tests for requested test types.
      2. Validates the generated tests using post-processors.
      3. Aggregates and returns the final test suites.
    """

    def __init__(self, adapter, unified_spec: dict, generation_params: dict = None):
        """
        :param adapter: An AI adapter instance (implements complete()).
        :param unified_spec: A normalized specification as a dictionary.
        :param generation_params: Optional default parameters (e.g., temperature, max_tokens).
        """
        self.adapter = adapter
        self.unified_spec = unified_spec
        self.generation_params = generation_params or {}

        # Mapping of test type to generator class.
        self.generator_mapping = {
            "functional": FunctionalTestGenerator,
            "security": SecurityTestGenerator,
            "performance": PerformanceTestGenerator,
            "e2e": E2ETestGenerator
        }

    def run(self, test_types: list) -> dict:
        """
        Runs the test generation and post-processing for each requested test type.
        
        :param test_types: List of test types (e.g., ["functional", "security"]).
        :return: A dictionary with the processed test suites for each test type.
        """
        results = {}
        test_files = {}

        for test_type in test_types:
            generator_class = self.generator_mapping.get(test_type)
            if not generator_class:
                logger.warning(f"No generator found for test type: {test_type}. Skipping.")
                continue

            generator = generator_class(self.adapter)
            logger.info(f"Generating {test_type} tests...")
            test_suite = generator.generate(self.unified_spec, **self.generation_params)
            logger.info(f"{test_type} tests generated.")

            # Post processing: Syntax check, spec compliance, and security scan
            test_code = test_suite.get("generated_tests", "")
            
            if test_code:
                # Store test code with type-specific filename
                filename = self._get_filename_for_type(test_type)
                test_files[filename] = test_code

            # Syntax Check
            try:
                logger.info(f"Running syntax check for {test_type} tests...")
                check_syntax(test_code)
                logger.info("Syntax check passed.")
            except Exception as e:
                logger.error(f"Syntax check failed for {test_type} tests: {e}")
                test_suite["syntax_errors"] = str(e)

            # Specification Compliance Check
            try:
                logger.info(f"Running spec compliance check for {test_type} tests...")
                check_spec_compliance(test_suite, self.unified_spec)
                logger.info("Spec compliance check passed.")
            except Exception as e:
                logger.error(f"Spec compliance check failed for {test_type} tests: {e}")
                test_suite["spec_compliance_errors"] = str(e)

            # Security Scan
            logger.info(f"Scanning {test_type} tests for security issues...")
            security_issues = scan_security(test_code)
            if security_issues:
                logger.warning(f"Security issues found: {security_issues}")
                test_suite["security_issues"] = security_issues
            else:
                logger.info("No security issues found.")

            results[test_type] = test_suite

        results["test_files"] = test_files
        return results

    def _get_filename_for_type(self, test_type: str) -> str:
        """Map test types to filenames"""
        filenames = {
            "functional": "functional_api_tests.py",
            "security": "security_tests.py",
            "performance": "performance_tests.py",
            "e2e": "e2e_tests.py"
        }
        return filenames.get(test_type, f"{test_type}_tests.py")

# Standalone demo when running orchestrator.py directly.
if __name__ == "__main__":
    # Dummy unified specification for demonstration.
    dummy_spec = {
        "title": "Demo API",
        "endpoints": [
            {"path": "/login", "method": "POST", "description": "User login"},
            {"path": "/logout", "method": "POST", "description": "User logout"}
        ]
    }
    # For demonstration, use the HuggingFace adapter.
    from ai_engine.adapters.huggingface_adapter import HuggingFaceAdapter
    adapter = HuggingFaceAdapter(model="gpt2")

    orchestrator = Orchestrator(adapter, dummy_spec, generation_params={"max_length": 200, "temperature": 0.7})
    final_results = orchestrator.run(["functional", "security", "performance", "e2e"])
    print("Final Generated Test Suites:")
    for test_type, suite in final_results.items():
        print(f"\n--- {test_type.upper()} TESTS ---")
        print(suite)

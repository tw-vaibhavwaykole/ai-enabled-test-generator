# ai-test-generator/ai_engine/post_processor/spec_compliance.py

def check_spec_compliance(test_suite: dict, unified_spec: dict) -> bool:
    """
    Checks whether the generated test suite complies with the given specification.
    For example, ensures that all endpoints defined in the spec are mentioned in the test code.
    
    :param test_suite: The generated test suite as a dictionary.
    :param unified_spec: The unified specification as a dictionary.
    :return: True if compliant; otherwise, raises an exception.
    """
    tests_text = test_suite.get("generated_tests", "")
    if not tests_text:
        raise ValueError("Generated tests are empty.")

    endpoints = unified_spec.get("endpoints", [])
    missing_endpoints = []
    for endpoint in endpoints:
        path = endpoint.get("path")
        if path not in tests_text:
            missing_endpoints.append(path)

    if missing_endpoints:
        raise ValueError(f"Test suite does not cover the following endpoints: {missing_endpoints}")

    return True

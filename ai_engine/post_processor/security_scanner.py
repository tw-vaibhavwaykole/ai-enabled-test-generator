# ai-test-generator/ai_engine/post_processor/security_scanner.py

def scan_security(test_code: str) -> list:
    """
    Scans the generated test code for potential security issues.
    This is a simulated scanner that checks for risky patterns.
    
    :param test_code: The test code as a string.
    :return: A list of security issues found (empty if none).
    """
    issues = []

    # Example check: flag usage of eval(), which can be a security risk.
    if "eval(" in test_code:
        issues.append("Usage of eval() detected, which is a potential security risk.")

    # More security checks can be added here.
    return issues

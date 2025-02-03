# ai-test-generator/ai_engine/post_processor/syntax_checker.py

def check_syntax(test_code: str) -> bool:
    """
    Performs a basic syntax check on the generated test code.
    For Python code, this attempts to compile the code.
    
    :param test_code: The test code as a string.
    :return: True if syntax is correct; otherwise, raises an exception.
    """
    if not test_code or not isinstance(test_code, str):
        raise ValueError("Test code is empty or not a string.")

    try:
        compile(test_code, "<string>", "exec")
    except Exception as e:
        raise SyntaxError(f"Syntax error in test code: {e}")

    return True

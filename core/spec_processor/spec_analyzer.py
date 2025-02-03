# ai-test-generator/core/spec_processor/spec_analyzer.py

def analyze_spec(spec: dict) -> dict:
    """
    Analyzes the given specification and extracts key details.
    For an OpenAPI spec, it extracts the endpoints and their HTTP methods.

    :param spec: The specification as a dictionary.
    :return: A dictionary with analysis details (e.g., list of endpoints).
    """
    analysis = {}
    endpoints = []

    # OpenAPI specs typically define endpoints under the "paths" key.
    paths = spec.get("paths", {})
    for path, methods in paths.items():
        for method in methods.keys():
            endpoints.append({"path": path, "method": method.upper()})
    
    analysis["endpoints"] = endpoints
    return analysis

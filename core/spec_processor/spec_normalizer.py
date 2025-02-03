# ai-test-generator/core/spec_processor/spec_normalizer.py

from .spec_analyzer import analyze_spec

def normalize_spec(spec: dict) -> dict:
    """
    Normalizes the given specification into a unified format.
    For an OpenAPI spec, extracts the API title, version, and endpoints.

    :param spec: The original specification as a dictionary.
    :return: A normalized specification as a dictionary.
    """
    unified_spec = {}

    if "openapi" in spec:
        # Extract basic API info.
        info = spec.get("info", {})
        unified_spec["title"] = info.get("title", "Untitled API")
        unified_spec["version"] = info.get("version", "unknown")

        # Use the analyzer to extract endpoints.
        analysis = analyze_spec(spec)
        unified_spec.update(analysis)
    else:
        # For other spec types, one might add additional normalization logic.
        unified_spec = spec  # Fallback to original spec.
    
    return unified_spec

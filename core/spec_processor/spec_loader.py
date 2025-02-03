# ai-test-generator/core/spec_processor/spec_loader.py

import os
from .openapi_validator import load_spec as load_openapi_spec, validate_openapi_spec

def load_spec(file_path: str) -> dict:
    """
    Loads a specification from the given file path.
    Supports JSON and YAML formats.
    If the spec contains an "openapi" key, it is treated as an OpenAPI spec and validated.

    :param file_path: Path to the specification file.
    :return: The loaded specification as a dictionary.
    :raises FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Specification file '{file_path}' not found.")

    spec = load_openapi_spec(file_path)

    # If this looks like an OpenAPI spec, validate it.
    if "openapi" in spec:
        validate_openapi_spec(spec)

    return spec

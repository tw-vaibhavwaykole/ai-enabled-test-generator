# ai-test-generator/core/spec_processor/openapi_validator.py

import json
import yaml
from openapi_spec_validator import validate_spec
from openapi_spec_validator.exceptions import OpenAPIValidationError

def load_spec(file_path: str) -> dict:
    """
    Loads an OpenAPI specification from a JSON or YAML file.

    :param file_path: Path to the specification file.
    :return: The specification as a dictionary.
    :raises ValueError: If the file extension is unsupported.
    """
    if file_path.endswith(".json"):
        with open(file_path, "r", encoding="utf-8") as f:
            spec = json.load(f)
    elif file_path.endswith((".yaml", ".yml")):
        with open(file_path, "r", encoding="utf-8") as f:
            spec = yaml.safe_load(f)
    else:
        raise ValueError("Unsupported file type. Only JSON and YAML are supported.")
    return spec

def validate_openapi_spec(spec: dict) -> bool:
    """
    Validates the given OpenAPI specification.

    :param spec: The OpenAPI specification as a dictionary.
    :return: True if the spec is valid.
    :raises ValueError: If the spec is invalid.
    """
    try:
        validate_spec(spec)
        return True
    except OpenAPIValidationError as e:
        raise ValueError(f"Invalid OpenAPI specification: {e}") from e

# ai-test-generator/core/test_models/test_case.py

from dataclasses import dataclass, field

@dataclass
class TestCase:
    """
    Represents a single test case.
    """
    name: str
    description: str = ""
    test_code: str = ""
    metadata: dict = field(default_factory=dict)

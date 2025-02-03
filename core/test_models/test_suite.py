# ai-test-generator/core/test_models/test_suite.py

from dataclasses import dataclass, field
from typing import List
from .test_case import TestCase

@dataclass
class TestSuite:
    """
    Represents a collection of test cases.
    """
    name: str
    test_cases: List[TestCase] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def add_test_case(self, test_case: TestCase) -> None:
        """
        Adds a new test case to the suite.
        
        :param test_case: An instance of TestCase to be added.
        """
        self.test_cases.append(test_case)

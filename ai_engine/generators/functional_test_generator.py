# ai-test-generator/ai_engine/generators/functional_test_generator.py

from ai_engine.generators.base_generator import BaseGenerator
from typing import List, Dict
import os

class FunctionalTestGenerator(BaseGenerator):
    """Generator for creating functional test cases based on a unified specification."""

    def __init__(self, adapter, prompt_template: str = None):
        prompt_template = prompt_template or """Generate comprehensive functional tests with Allure reporting in pytest format for this API spec:
{spec}

Requirements:
1. Include standard imports and fixtures as needed.

2. Generate functional test scenarios for:

CRUD Operations:
- Create (single, bulk, with relationships)
- Read (by ID, filtered, paginated)
- Update (full, partial, conditional)
- Delete (single, bulk, cascade)
- Batch operations
- Complex queries
- Search functionality
- Export/import operations

Data Validation:
- Field type validation
- Required fields
- Optional fields
- Field dependencies
- Complex validation rules
- Custom validators
- Format validation
- Range validation
- Pattern matching
- Unique constraints
- Foreign key constraints
- Composite key validation

Query Parameters:
- Filtering (single, multiple, complex)
- Sorting (single, multiple fields)
- Pagination (offset, cursor-based)
- Field selection
- Include/exclude fields
- Relationship expansion
- Search parameters
- Date range filters
- Geo-spatial queries
- Full-text search

Response Validation:
- Status codes
- Response headers
- Content types
- Data structure
- Field presence
- Data types
- Relationships
- Calculated fields
- Aggregations
- Metadata
- Error formats

Business Logic:
- Workflow validation
- State transitions
- Business rules
- Calculations
- Data transformations
- Conditional logic
- Complex operations
- Multi-step processes
- Async operations
- Background jobs

Edge Cases:
- Boundary values
- Empty/null values
- Special characters
- Unicode handling
- Large datasets
- Minimal datasets
- Duplicate handling
- Race conditions
- Timeout scenarios
- Network issues

Performance Scenarios:
- Response times
- Bulk operations
- Concurrent requests
- Resource usage
- Cache behavior
- Database load
- Memory usage
- Connection pooling
- Query optimization
- Resource cleanup

Integration Points:
- External services
- Database operations
- Cache interactions
- File operations
- Message queues
- Event handling
- Webhooks
- Third-party APIs
- Authentication services
- Storage services

3. Each test should include:
- Clear test steps
- Data setup/teardown
- Comprehensive assertions
- Error handling
- Response validation
- Performance checks
- Resource cleanup
- State verification

4. Use dynamic test data:
- Data generators
- Randomized inputs
- Boundary values
- Valid/invalid combinations
- Complex scenarios
- Real-world examples
- Edge cases
- Load testing data

5. Include proper test organization:
- Logical grouping
- Dependencies
- Setup/teardown
- Shared fixtures
- Resource management
- State handling
- Error recovery
- Cleanup procedures

Return the complete test suite with proper organization and documentation.
"""
        super().__init__(adapter, prompt_template)
        self.test_type = "functional"

    def generate(self, unified_spec: dict, **kwargs):
        """Generate functional test cases using AI."""
        try:
            # Compose the prompt with the API spec
            prompt = self._compose_prompt(unified_spec)
            
            # Get the AI-generated response with increased token limit
            response = self.adapter.complete(
                prompt,
                max_tokens=4000,  # Increased for more comprehensive tests
                temperature=0.7,
                **kwargs
            )
            
            # Parse and clean the response
            parsed_tests = self._parse_output(response)
            
            # Write the generated tests to file
            output_dir = kwargs.get('output_dir', 'artifacts/generated_tests')
            os.makedirs(output_dir, exist_ok=True)
            
            test_code = self._format_test_code(parsed_tests[0]["test_code"] if parsed_tests else "")
            output_path = os.path.join(output_dir, 'functional_api_tests.py')
            
            with open(output_path, 'w') as f:
                f.write(test_code)
            
            return {
                "type": "functional",
                "spec_summary": unified_spec,
                "generated_tests": test_code,
                "output_path": output_path
            }
        except Exception as e:
            print(f"Error generating functional tests: {str(e)}")
            raise

    def validate(self, tests: List[Dict]) -> bool:
        """Validate functional tests meet basic requirements"""
        if not tests:
            return False
        return all(
            isinstance(test, dict) and 
            test.get("name") and 
            test.get("test_code")
            for test in tests
        )

    def _parse_output(self, raw_output: str) -> List[Dict]:
        """Parse raw output into executable pytest code"""
        # Extract code blocks from markdown response if present
        code_blocks = []
        current_block = []
        in_code = False
        
        # Split the response into lines
        lines = raw_output.split('\n')
        
        # If the response doesn't contain markdown code blocks, treat it as pure code
        if not any(line.strip().startswith('```') for line in lines):
            return [{
                "name": "functional_tests",
                "test_code": raw_output,
                "tags": ["functional"]
            }]
        
        # Process markdown code blocks
        for line in lines:
            if line.strip().startswith('```python'):
                in_code = True
                continue
            elif line.strip().startswith('```'):
                in_code = False
                if current_block:
                    code_blocks.append('\n'.join(current_block))
                current_block = []
                continue
            elif in_code:
                current_block.append(line)
        
        if current_block:
            code_blocks.append('\n'.join(current_block))
        
        # Combine all code blocks
        combined_code = '\n'.join(code_blocks)
        
        return [{
            "name": "functional_tests",
            "test_code": combined_code,
            "tags": ["functional"]
        }]

    def _format_test_code(self, test_code: str) -> str:
        """Format and clean the test code"""
        # Required imports in correct order
        basic_imports = [
            'from typing import Dict, List',
            'import json',
            'import pytest',
            'import requests',
            'import allure',
            '',  # Empty line after imports
        ]
        
        # Fix allure decorator patterns
        test_code = test_code.replace('@allure.severity(allure.severity_level.', '@allure.')
        test_code = test_code.replace('@allure_feature', '@allure.feature')
        test_code = test_code.replace('@allure_story', '@allure.story')
        test_code = test_code.replace('@allure_severity', '@allure.severity')
        test_code = test_code.replace('@allure_description', '@allure.description')
        
        # Fix severity level references
        test_code = test_code.replace('severity_level.CRITICAL', 'severity_level.CRITICAL')
        test_code = test_code.replace('severity_level.NORMAL', 'severity_level.NORMAL')
        test_code = test_code.replace('severity_level.MINOR', 'severity_level.MINOR')
        
        lines = test_code.split('\n')
        imports_seen = set()
        fixtures_seen = set()
        clean_lines = []
        
        # Process lines
        for line in lines:
            # Skip duplicate imports
            if line.startswith('import ') or line.startswith('from '):
                if line not in imports_seen:
                    imports_seen.add(line)
                continue
            
            # Handle fixtures
            if '@pytest.fixture' in line:
                fixture_def = next((l for l in lines[lines.index(line):] if l.startswith('def ')), '')
                if fixture_def and fixture_def not in fixtures_seen:
                    fixtures_seen.add(fixture_def)
                    clean_lines.extend(['', line, fixture_def])  # Add empty line before fixture
                continue
            
            # Add other lines if they're not part of a fixture we've already seen
            if not any(fixture in line for fixture in fixtures_seen):
                clean_lines.append(line)
        
        # Combine imports and cleaned lines
        final_lines = []
        for imp in basic_imports:
            if imp not in imports_seen:
                final_lines.append(imp)
        
        # Add the rest of the code
        final_lines.extend(line for line in clean_lines if line.strip())
        
        return '\n'.join(final_lines)

    def _fix_syntax(self, line: str) -> str:
        """Attempt to fix common syntax issues in a line of code"""
        # Fix unterminated strings
        if line.count("'") % 2 == 1:
            line = line + "'"
        if line.count('"') % 2 == 1:
            line = line + '"'
        
        # Fix incomplete dictionary literals
        if line.strip().endswith('{'):
            line = line + '}'
        if line.strip().endswith(': '):
            line = line + "'value'"
        
        try:
            # Verify the fix worked
            compile(line, '<string>', 'exec')
            return line
        except SyntaxError:
            return None

    def _generate_basic_functional_tests(self) -> str:
        """Generate basic functional test structure"""
        return '''import pytest
import requests
import allure

def test_get_pets(base_url, headers):
    """Test retrieving list of pets"""
    response = requests.get(f'{base_url}/pets', headers=headers)
    assert response.status_code == 200
    assert 'application/json' in response.headers['Content-Type']

def test_add_pet(base_url, headers):
    """Test adding a new pet"""
    new_pet = {'name': 'TestPet', 'status': 'available'}
    response = requests.post(f'{base_url}/pets', json=new_pet, headers=headers)
    assert response.status_code == 201
'''

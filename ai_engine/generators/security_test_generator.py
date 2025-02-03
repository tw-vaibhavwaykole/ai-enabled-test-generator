# ai-test-generator/ai_engine/generators/security_test_generator.py

from ai_engine.generators.base_generator import BaseGenerator
from typing import List, Dict
import os

class SecurityTestGenerator(BaseGenerator):
    """
    Generator for creating security test cases based on a unified specification.
    """

    def __init__(self, adapter, prompt_template: str = None):
        prompt_template = prompt_template or """Generate comprehensive security tests with Allure reporting in pytest format for this API spec:
{spec}

Requirements:
1. Include standard imports and fixtures as needed.

2. Generate security test scenarios for the following categories:

Authentication & Authorization:
- Token validation (valid, invalid, expired, malformed)
- OAuth2 flows (if applicable)
- API key validation
- Session management
- Role-based access (admin, user, guest)
- Permission boundaries
- Token refresh mechanisms
- Multi-factor authentication bypass attempts
- Session fixation tests
- Cookie security tests

Input Validation & Injection:
- SQL injection (various payloads)
- NoSQL injection
- XSS (reflected, stored, DOM)
- XML injection
- XPATH injection
- LDAP injection
- Command injection
- Template injection
- Buffer overflow attempts
- Format string attacks
- Unicode injection
- HTML injection
- CSV injection
- File path manipulation
- ZIP bomb detection

API Security:
- Rate limiting bypass attempts
- Brute force protection
- Request throttling
- API versioning security
- GraphQL depth/complexity limits
- Batch request limits
- Race condition tests
- Cache poisoning
- Method tampering
- Content-type manipulation

Data Protection:
- PII data exposure
- Sensitive data in logs
- Cache-control headers
- Secure transmission tests
- Data encryption validation
- Backup data exposure
- Temporary file exposure
- Memory dumps
- Debug information exposure
- Error message information disclosure

Infrastructure Security:
- SSL/TLS verification
- Certificate validation
- CORS policy validation
- Security headers (CSP, HSTS, etc)
- HTTP method restrictions
- Server information disclosure
- Directory traversal
- File upload vulnerabilities
- WebSocket security
- Service worker security

Business Logic:
- Parameter tampering
- State manipulation
- Logic bypass attempts
- Workflow bypass
- Access control bypass
- Data validation bypass
- Business constraint bypass
- Time-based attacks
- Resource limits
- Transaction security

Compliance & Standards:
- OWASP Top 10 coverage
- GDPR requirements
- PCI DSS validation
- HIPAA compliance
- SOC2 requirements
- ISO27001 controls
- NIST guidelines
- CWE verification

3. Each test should include:
- Detailed test steps using allure.step
- Comprehensive assertions
- Security payload variations
- Response validation
- Error scenario handling
- Security header validation
- Timing attack detection
- Resource cleanup
- Test data isolation

4. Use dynamic test data:
- Generate unique test data
- Use security payload generators
- Implement different attack vectors
- Vary request parameters
- Test boundary conditions
- Include edge cases
- Use fuzzing techniques

5. Include proper error handling and cleanup:
- Resource cleanup after tests
- State reset between tests
- Exception handling
- Timeout handling
- Connection error handling
- Retry mechanisms
- Rollback procedures

Return the complete test suite with proper organization and documentation.
"""
        super().__init__(adapter, prompt_template)
        self.test_type = "security"

    def generate(self, unified_spec: dict, **kwargs):
        """Generate security test cases using AI."""
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
            output_path = os.path.join(output_dir, 'security_tests.py')
            
            with open(output_path, 'w') as f:
                f.write(test_code)
            
            return {
                "type": "security",
                "spec_summary": unified_spec,
                "generated_tests": test_code,
                "output_path": output_path
            }
        except Exception as e:
            print(f"Error generating security tests: {str(e)}")
            raise

    def validate(self, tests: List[Dict]) -> bool:
        """Validate security tests meet basic requirements"""
        if not tests:
            return False
        return all(
            isinstance(test, dict) and 
            test.get("name") and 
            test.get("test_code") and
            "security" in test.get("tags", [])
            for test in tests
        )

    def _parse_output(self, raw_output: str) -> List[Dict]:
        """Parse raw output into executable pytest code"""
        # Extract code blocks from markdown response
        code_blocks = []
        current_block = []
        in_code = False
        
        for line in raw_output.split('\n'):
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
        
        # If no code blocks found, return empty test structure
        if not code_blocks:
            return [{
                "name": "security_tests",
                "test_code": "import pytest\nimport requests\n\n",
                "tags": ["security"]
            }]
        
        # Combine all code blocks and add necessary imports
        combined_code = "import pytest\nimport requests\n\n"
        combined_code += "\n".join(code_blocks)
        
        return [{
            "name": "security_tests",
            "test_code": combined_code,
            "tags": ["security"]
        }]

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

    def _generate_basic_security_tests(self) -> str:
        """Generate basic security test structure"""
        return '''import pytest
import requests

@pytest.fixture
def base_url():
    return 'http://localhost:8080/api'

@pytest.fixture
def headers():
    return {'Content-Type': 'application/json'}

@pytest.fixture
def invalid_token():
    return {'Authorization': 'Bearer invalid_token'}

def test_unauthorized_access(base_url):
    """Test accessing protected endpoint without authentication"""
    response = requests.get(f'{base_url}/pets')
    assert response.status_code == 401

def test_invalid_authentication(base_url, invalid_token):
    """Test accessing protected endpoint with invalid token"""
    response = requests.get(f'{base_url}/pets', headers=invalid_token)
    assert response.status_code == 401

def test_sql_injection_prevention(base_url, headers):
    """Test SQL injection prevention"""
    malicious_id = "1' OR '1'='1"
    response = requests.get(f'{base_url}/pets/{malicious_id}', headers=headers)
    assert response.status_code in [400, 404]

def test_xss_prevention(base_url, headers):
    """Test XSS prevention"""
    malicious_data = {
        'name': '<script>alert("xss")</script>',
        'species': 'cat',
        'age': 3
    }
    response = requests.post(f'{base_url}/pets', headers=headers, json=malicious_data)
    assert response.status_code == 400

def test_rate_limiting(base_url, headers):
    """Test rate limiting"""
    for _ in range(100):  # Make multiple rapid requests
        response = requests.get(f'{base_url}/pets', headers=headers)
    assert response.status_code == 429

def test_method_not_allowed(base_url, headers):
    """Test HTTP method restrictions"""
    response = requests.patch(f'{base_url}/pets/1', headers=headers)
    assert response.status_code == 405
'''

    def _format_test_code(self, test_code: str) -> str:
        """Format and clean the test code"""
        # Required imports in correct order
        basic_imports = [
            'from typing import Dict, List',
            'import json',
            'import time',
            'import jwt',
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

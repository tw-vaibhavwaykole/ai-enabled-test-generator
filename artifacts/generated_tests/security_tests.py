import pytest
import requests
import allure

@pytest.fixture
def base_url():
    return 'http://localhost:8080/api'

@pytest.fixture
def headers():
    return {'Content-Type': 'application/json'}

from typing import Dict, List
import json
import time
import jwt

# Constants
BASE_URL = 'https://decision-delivery-internal.stage.ideasrms.com/api/v1'
# Fixtures for setup and teardown
@pytest.fixture(scope='module')
def get_auth_token():
    """Fixture to authenticate and return a valid token for use in tests."""
    response = requests.post(f"{BASE_URL}/auth", data={"username": "user", "password": "pass"})
    return response.json()['token']
@pytest.fixture(scope='function')
def setup_data():
    """Fixture to setup test data before each test."""
    # Setup test data or configurations
    yield
    # Teardown test data or configurations
# Example of a security test for API key validation
@allure.feature('Authentication & Authorization')
@allure.story('API Key Validation')
@allure.severity(Severity.CRITICAL)
def test_api_key_validation(get_auth_token):
    api_key = get_auth_token
    headers = {'Authorization': f'Bearer {api_key}'}
    with allure.step('Make a request with a valid API key'):
        response = requests.get(f"{BASE_URL}/endpoint", headers=headers)
        assert response.status_code == 200, "API key should be valid"
    with allure.step('Make a request with an invalid API key'):
        headers['Authorization'] = 'Bearer invalid_key'
        response = requests.get(f"{BASE_URL}/endpoint", headers=headers)
        assert response.status_code == 401, "Should reject invalid API key"
# Example of a security test for SQL injection
@allure.feature('Input Validation & Injection')
@allure.story('SQL Injection')
@allure.severity(Severity.HIGH)
def test_sql_injection(get_auth_token):
    headers = {'Authorization': f'Bearer {get_auth_token}'}
    malicious_payload = "' OR '1'='1"
    with allure.step('Attempt SQL injection'):
        response = requests.get(f"{BASE_URL}/endpoint?param={malicious_payload}", headers=headers)
        assert response.status_code == 400, "Should not be susceptible to SQL Injection"
# Example of a security test for checking HTTP method restrictions
@allure.feature('Infrastructure Security')
@allure.story('HTTP Method Restrictions')
@allure.severity(Severity.MEDIUM)
def test_http_method_restrictions(get_auth_token):
    headers = {'Authorization': f'Bearer {get_auth_token}'}
    with allure.step('Check for allowed HTTP methods'):
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
        for method in methods:
            response = requests.request(method, f"{BASE_URL}/endpoint", headers=headers)
            if method == 'GET':
                assert response.status_code != 405, f"Method {method} should be allowed"
            else:
                assert response.status_code == 405, f"Method {method} should not be allowed"
# Run the test suite
if __name__ == "__main__":
    pytest.main()
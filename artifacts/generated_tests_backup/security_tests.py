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
BASE_URL = "https://decision-delivery-internal.stage.ideasrms.com/api/v1"
TOKEN = "your_access_token_here"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
# Fixtures for setup and teardown
@pytest.fixture(scope="module")
def get_auth_token():
    # Simulate getting an auth token
    return "example_token"
@pytest.fixture(scope="function")
def setup_teardown():
    # Setup before each test
    yield
    # Teardown after each test
    # This could include deleting test data or logging out sessions
    pass
# Authentication & Authorization Tests
@allure.feature('Authentication & Authorization')
@allure.story('Token Validation')
@pytest.mark.parametrize("token", ["valid_token", "expired_token", "malformed_token"])
def test_token_validation(token):
    with allure.step("Sending API request with token"):
        response = requests.get(f"{BASE_URL}/trackers/clientCode/propertyCode/correlationId", headers={"Authorization": f"Bearer {token}"})
    with allure.step("Checking the response status"):
        if token == "valid_token":
            assert response.status_code == 200
        else:
            assert response.status_code == 401
        allure.attach(str(response.json()), name="Response Body", attachment_type=AttachmentType.JSON)
# Input Validation & Injection Tests
@allure.feature('Input Validation & Injection')
@allure.story('SQL Injection')
def test_sql_injection(setup_teardown):
    malicious_input = "' OR '1'='1"
    with allure.step("Injecting SQL code"):
        response = requests.post(f"{BASE_URL}/trackers/clientCode/propertyCode/correlationId",
                                 json={"messageId": malicious_input}, headers=HEADERS)
    with allure.step("Verifying SQL injection is handled"):
        assert response.status_code == 400
        assert "error" in response.json()
        allure.attach(str(response.json()), name="Response Body", attachment_type=AttachmentType.JSON)
# API Security Tests
@allure.feature('API Security')
@allure.story('Rate Limiting Bypass Attempts')
def test_rate_limiting(setup_teardown):
    with allure.step("Simulate multiple rapid requests to test rate limiting"):
        responses = [requests.get(f"{BASE_URL}/trackers/clientCode/propertyCode/correlationId", headers=HEADERS) for _ in range(100)]
    with allure.step("Verifying rate limiting response"):
        # Assuming that the API implements rate limiting after 50 requests per minute
        assert any([resp.status_code == 429 for resp in responses])
        allure.attach(str([resp.status_code for resp in responses]), name="Status Codes", attachment_type=AttachmentType.TEXT)
# Data Protection Tests
@allure.feature('Data Protection')
@allure.story('PII Data Exposure')
def test_pii_data_exposure(setup_teardown):
    with allure.step("Requesting sensitive data"):
        response = requests.get(f"{BASE_URL}/trackers/clientCode/propertyCode/correlationId", headers=HEADERS)
    with allure.step("Checking for PII data in response"):
        # Example assertion to check PII data is not exposed
        assert "socialSecurityNumber" not in response.text
        allure.attach(str(response.json()), name="Response Body", attachment_type=AttachmentType.JSON)
# Usage
# To run the tests and generate an Allure report:
# pytest --alluredir=/path/to/allure/results
# allure serve /path/to/allure/results
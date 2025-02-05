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
import time
import jwt

# Constants
BASE_URL = "http://localhost:8080/api"
API_KEY = "valid_api_key"  # Assume this is a valid API key for authenticated requests
# Test Data Generator
fake = Faker()
# Fixtures and Helpers
@pytest.fixture(scope="module")
def get_api_key():
    return API_KEY
@pytest.fixture(scope="function")
def create_pet():
    """Fixture to create a pet using valid API credentials."""
    pet = {
        "id": fake.random_int(min=1, max=1000),
        "name": fake.name(),
        "status": "available"
    }
    response = requests.post(f"{BASE_URL}/pets", headers={"X-API-Key": API_KEY}, json=pet)
    yield pet
    # Cleanup
    requests.delete(f"{BASE_URL}/pets/{pet['id']}", headers={"X-API-Key": API_KEY})
# API Key Validation
@allure.severity(Severity.CRITICAL)
@allure.title("Test API Key Validation: Invalid API Key")
def test_api_key_validation_invalid():
    with allure.step("Make API request with invalid API key"):
        response = requests.get(f"{BASE_URL}/pets", headers={"X-API-Key": "invalid_key"})
        assert response.status_code == 401, "Expected a 401 Unauthorized status code for invalid API key"
# Input Validation & Injection
@allure.severity(Severity.HIGH)
@allure.title("Test SQL Injection on the 'pets' endpoint")
@pytest.mark.parametrize("injection_string", ["1; DROP TABLE users", "' OR '1'='1"])
def test_sql_injection_pets_endpoint(injection_string):
    with allure.step("Attempt SQL injection"):
        response = requests.get(f"{BASE_URL}/pets", params={"limit": injection_string}, headers={"X-API-Key": API_KEY})
        assert response.status_code == 400, "Expected a 400 Bad Request status code for SQL injection attempt"
# API Security: Rate Limiting
@allure.severity(Severity.NORMAL)
@allure.title("Test Rate Limiting by sending rapid successive requests")
def test_rate_limiting():
    with allure.step("Send multiple requests to test rate limiting"):
        for _ in range(20):
            response = requests.get(f"{BASE_URL}/pets", headers={"X-API-Key": API_KEY})
            if response.status_code == 429:
                break
        assert response.status_code == 429, "Expected a 429 Too Many Requests status code for rate limiting test"
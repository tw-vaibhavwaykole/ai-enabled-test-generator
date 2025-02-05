import pytest
import requests

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

fake = Faker()
@pytest.fixture
def api_url():
    return 'http://localhost:8080/api'
def api_key():
    return 'test_api_key'
@allure.title("Token Validation Test")
def test_token_validation():
    pass
    # Add test steps, assertions, and security payload variations
@allure.title("OAuth2 Flows Test")
def test_oauth2_flows():
    pass
    # Add test steps, assertions, and security payload variations
@allure.title("API Key Validation Test")
def test_api_key_validation(api_key):
    pass
    # Add test steps, assertions, and security payload variations
@allure.title("Session Management Test")
def test_session_management():
    pass
    # Add test steps, assertions, and security payload variations
@allure.title("Role-Based Access Test")
def test_role_based_access():
    pass
    # Add test steps, assertions, and security payload variations
# Add more security test scenarios for other categories
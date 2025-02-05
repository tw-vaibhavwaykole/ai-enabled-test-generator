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
import allure

# Constants
BASE_URL = "http://localhost:8080/api"
# Fixtures for session, authorization, and test data setup
@pytest.fixture(scope="module")
def get_api_key():
    # placeholder for getting the API key
    return "your_api_key"
@pytest.fixture(scope="function")
def create_pet(get_api_key):
    """Fixture to create a pet before tests and delete it afterwards."""
    url = f"{BASE_URL}/pets"
    headers = {"X-API-Key": get_api_key}
    pet_data = {"id": 1, "name": "Buddy", "status": "available"}
    response = requests.post(url, headers=headers, json=pet_data)
    yield response.json()
    # Teardown: delete the pet
    requests.delete(f"{url}/{pet_data['id']}", headers=headers)
# Test functions with Allure decorators
@allure.feature('Pets')
@allure.story('Create, Retrieve, Update, Delete (CRUD)')
def test_add_pet(get_api_key):
    """Test adding a new pet."""
    url = f"{BASE_URL}/pets"
    headers = {"X-API-Key": get_api_key}
    pet_data = {"id": 2, "name": "Charlie", "status": "available"}
    with allure.step("Create a new pet"):
        response = requests.post(url, headers=headers, json=pet_data)
        assert response.status_code == 201
    with allure.step("Check the pet was added correctly"):
        get_response = requests.get(f"{url}/{pet_data['id']}", headers=headers)
        assert get_response.status_code == 200
        assert get_response.json()['name'] == pet_data['name']
@pytest.mark.usefixtures("create_pet")
@allure.feature('Pets')
@allure.story('Validation')
def test_get_pet_by_id(create_pet, get_api_key):
    """Test retrieving a pet by ID."""
    pet = create_pet
    url = f"{BASE_URL}/pets/{pet['id']}"
    headers = {"X-API-Key": get_api_key}
    with allure.step("Retrieve the pet by ID"):
        response = requests.get(url, headers=headers)
        assert response.status_code == 200
        assert response.json()['id'] == pet['id']
# More tests for update, delete, complex queries, and other operations can be added following the above pattern
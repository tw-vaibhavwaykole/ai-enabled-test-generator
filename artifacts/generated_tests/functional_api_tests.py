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
import allure

fake = Faker()
@pytest.fixture
def base_url():
    return 'http://localhost:8080/api'
def auth_header():
    return {'X-API-Key': 'your_api_key'}
# Helper functions
def create_pet(payload):
    response = requests.post(f'{base_url()}/pets', json=payload)
    return response.json()
def get_pet_by_id(pet_id):
    response = requests.get(f'{base_url()}/pets/{pet_id}')
    return response.json()
# CRUD Operations
@pytest.mark.parametrize('payload', [{'name': fake.name(), 'age': fake.random_int(min=1, max=10), 'status': 'available'}])
def test_create_pet(payload, base_url, auth_header):
    response = create_pet(payload)
    assert response['name'] == payload['name']
    assert response['status'] == payload['status']
def test_read_pet_by_id(base_url, auth_header):
    pet_id = 1
    response = get_pet_by_id(pet_id)
    assert response['id'] == pet_id
# Data Validation
def test_field_type_validation():
    payload = {'name': fake.name(), 'age': 'invalid', 'status': 'available'}
    with pytest.raises(TypeError):
        create_pet(payload)
def test_required_fields():
    payload = {'age': 5, 'status': 'available'}
    with pytest.raises(Exception):
        create_pet(payload)
# Query Parameters
def test_filtering():
    response = requests.get(f'{base_url()}/pets?status=available')
    assert all(pet['status'] == 'available' for pet in response.json())
# Response Validation
def test_status_codes():
    response = requests.get(f'{base_url()}/pets')
    assert response.status_code == 200
# Business Logic
def test_workflow_validation():
    payload = {'name': fake.name(), 'age': 5, 'status': 'pending'}
    response = create_pet(payload)
    assert response['status'] == 'pending'
# Edge Cases
def test_empty_values():
    payload = {'name': ''}
    with pytest.raises(Exception):
        create_pet(payload)
# Performance Scenarios
def test_response_times():
    response = requests.get(f'{base_url()}/pets')
    assert response.elapsed.total_seconds() < 1
# Integration Points
def test_database_operations():
    response = requests.get(f'{base_url()}/pets')
    assert len(response.json()) > 0
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
import allure

fake = Faker()
# Base URL for the API
BASE_URL = "https://decision-delivery-internal.stage.ideasrms.com/api/v1"
# Fixtures for setup and teardown of data
@pytest.fixture(scope="function")
def create_tracker():
    """Create a tracker and return its ID for further testing."""
    data = {
        "clientCode": fake.word(),
        "propertyCode": fake.word(),
        "correlationId": fake.uuid4(),
        "messageId": fake.uuid4(),
        # additional fields
    }
    response = requests.post(f"{BASE_URL}/decisiondelivery/trackers/", json=data)
    yield response.json()['id']
    # Teardown: delete the tracker
    requests.delete(f"{BASE_URL}/decisiondelivery/trackers/{response.json()['id']}")
@allure.feature('CRUD Operations')
@allure.story('Create a new tracker')
def test_create_tracker():
    with step("Create a tracker"):
        tracker_data = {
            "clientCode": fake.word(),
            "propertyCode": fake.word(),
            "correlationId": fake.uuid4(),
            "messageId": fake.uuid4(),
            # additional required fields
        }
        response = requests.post(f"{BASE_URL}/decisiondelivery/trackers/", json=tracker_data)
        assert response.status_code == 201, "Check that the tracker is created"
        assert 'id' in response.json(), "Verify that the returned data includes a 'id' field"
@allure.feature('CRUD Operations')
@allure.story('Read a tracker')
def test_read_tracker(create_tracker):
    tracker_id = create_tracker
    with step("Read the tracker"):
        response = requests.get(f"{BASE_URL}/decisiondelivery/trackers/{tracker_id}")
        assert response.status_code == 200, "Check that the tracker is fetched successfully"
        assert response.json()['id'] == tracker_id, "Verify the tracker ID matches"
@allure.feature('CRUD Operations')
@allure.story('Update a tracker')
def test_update_tracker(create_tracker):
    tracker_id = create_tracker
    new_data = {"status": "SUCCESS"}
    with step("Update the tracker"):
        response = requests.patch(f"{BASE_URL}/decisiondelivery/trackers/{tracker_id}", json=new_data)
        assert response.status_code == 200, "Check that the update is successful"
        assert response.json()['status'] == "SUCCESS", "Verify that the status is updated"
@allure.feature('Data Validation')
@allure.story('Validate required fields for tracker creation')
def test_validate_required_fields():
    with step("Attempt to create tracker without required fields"):
        tracker_data = {
            # Missing required fields
        }
        response = requests.post(f"{BASE_URL}/decisiondelivery/trackers/", json=tracker_data)
        assert response.status_code == 400, "Check that the request fails without required fields"
        assert 'error' in response.json(), "Verify that an error message is returned"
@allure.feature('Query Parameters')
@allure.story('Filter trackers by status')
def test_filter_trackers_by_status():
    status = "PENDING"
    with step("Filter trackers by status"):
        response = requests.get(f"{BASE_URL}/decisiondelivery/trackers/", params={"status": status})
        assert response.status_code == 200, "Check that the request is successful"
        assert all(tracker['status'] == status for tracker in response.json()), "Verify all trackers have the correct status"
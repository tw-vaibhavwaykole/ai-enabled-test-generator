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

# Import necessary libraries
# Common fixtures
@pytest.fixture(scope="module")
def base_url():
    return "https://decision-delivery-internal.stage.ideasrms.com"
@pytest.fixture(scope="session")
def api_headers():
    return {"Content-Type": "application/json", "Accept": "application/json"}
def get_auth_token():
    # Mock authentication token retrieval
    return "mock_token"
@allure.feature('CRUD Operations')
class TestDecisionDeliveryTrackerCRUD:
    @allure.story('Create Decision Delivery Tracker')
    @pytest.mark.parametrize("data", [
        {"clientCode": "testClient", "propertyCode": "testProperty", "correlationId": "testCorrelation", "messageId": "1"},
        # Add more data sets for bulk creation
    ])
    def test_create_decision_delivery_tracker(self, base_url, api_headers, get_auth_token, data):
        url = f"{base_url}/api/v1/decisiondelivery/trackers/{data['clientCode']}/{data['propertyCode']}/{data['correlationId']}"
        api_headers['Authorization'] = f"Bearer {get_auth_token}"
        response = requests.post(url, headers=api_headers, json=[data])
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        # Further response validation goes here
    @allure.story('Read Decision Delivery Tracker')
    def test_read_decision_delivery_tracker(self, base_url, api_headers, get_auth_token):
        client_code = "testClient"
        property_code = "testProperty"
        correlation_id = "testCorrelation"
        url = f"{base_url}/api/v1/decisiondelivery/trackers/{client_code}/{property_code}/{correlation_id}"
        api_headers['Authorization'] = f"Bearer {get_auth_token}"
        response = requests.get(url, headers=api_headers)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        # Further response validation goes here
    @allure.story('Update Decision Delivery Tracker')
    def test_update_decision_delivery_tracker(self, base_url, api_headers, get_auth_token):
        client_code = "testClient"
        property_code = "testProperty"
        correlation_id = "testCorrelation"
        message_id = "1"
        url = f"{base_url}/api/v1/decisiondelivery/trackers/{client_code}/{property_code}/{correlation_id}/{message_id}"
        api_headers['Authorization'] = f"Bearer {get_auth_token}"
        new_data = {"status": "SUCCESS"}
        response = requests.patch(url, headers=api_headers, json=new_data)
        assert response.status_code == 200
        # Further response validation goes here
    @allure.story('Delete Decision Delivery Tracker')
    def test_delete_decision_delivery_tracker(self, base_url, api_headers, get_auth_token):
        client_code = "testClient"
        property_code = "testProperty"
        correlation_id = "testCorrelation"
        message_id = "1"
        url = f"{base_url}/api/v1/decisiondelivery/trackers/{client_code}/{property_code}/{correlation_id}/{message_id}"
        api_headers['Authorization'] = f"Bearer {get_auth_token}"
        response = requests.delete(url, headers=api_headers)
        assert response.status_code == 204
        # Further response validation goes here
@allure.feature('Data Validation')
class TestDataValidation:
    @allure.story('Validate Required Fields')
    def test_validate_required_fields(self, base_url, api_headers, get_auth_token):
        url = f"{base_url}/api/v1/decisiondelivery/trackers/testClient/testProperty/testCorrelation"
        api_headers['Authorization'] = f"Bearer {get_auth_token}"
        incomplete_data = {"clientCode": "onlyClientCode"}  # Missing other required fields
        response = requests.post(url, headers=api_headers, json=[incomplete_data])
        assert response.status_code == 400
        assert 'application/json' in response.headers['Content-Type']
        # Further error message validation goes here
@allure.feature('Complex Queries')
class TestComplexQueries:
    @allure.story('Filter and Sort')
    def test_filter_and_sort(self, base_url, api_headers, get_auth_token):
        url = f"{base_url}/api/v1/decisiondelivery/trackers/testClient/testProperty/testCorrelation"
        params = {
            "status": "PENDING",
            "sort": "messageId,desc",
            "page": 0,
            "size": 10
        }
        api_headers['Authorization'] = f"Bearer {get_auth_token}"
        response = requests.get(url, headers=api_headers, params=params)
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        # Validate sorting and pagination logic from response data
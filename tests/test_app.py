import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'ok'

def test_trace_endpoint_empty_input(client):
    response = client.post('/api/trace', json={'requirement': ''})
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data['success'] is False

def test_trace_endpoint_valid_requirement(client):
    response = client.post('/api/trace', json={
        'requirement': 'FUNC-101: Emergency Braking',
        'use_mock': True
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['root_item']['id'] == 'FUNC-101'
    assert len(json_data['linked_items']) > 0
    assert 'coverage' in json_data

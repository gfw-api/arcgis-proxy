import json

import RWAPIMicroservicePython
import pytest
import requests_mock

import arcgis_proxy

USERS = {
    "ADMIN": {
        "id": '1a10d7c6e0a37126611fd7a7',
        "role": 'ADMIN',
        "provider": 'local',
        "email": 'user@control-tower.org',
        "name": 'John Admin',
        "extraUserData": {
            "apps": [
                'rw',
                'gfw',
                'gfw-climate',
                'prep',
                'aqueduct',
                'forest-atlas',
                'data4sdgs'
            ]
        }
    },
    "MANAGER": {
        "id": '1a10d7c6e0a37126611fd7a7',
        "role": 'MANAGER',
        "provider": 'local',
        "email": 'user@control-tower.org',
        "extraUserData": {
            "apps": [
                'rw',
                'gfw',
                'gfw-climate',
                'prep',
                'aqueduct',
                'forest-atlas',
                'data4sdgs'
            ]
        }
    },
    "USER": {
        "id": '1a10d7c6e0a37126611fd7a7',
        "role": 'USER',
        "provider": 'local',
        "email": 'user@control-tower.org',
        "extraUserData": {
            "apps": [
                'rw',
                'gfw',
                'gfw-climate',
                'prep',
                'aqueduct',
                'forest-atlas',
                'data4sdgs'
            ]
        }
    },
    "MICROSERVICE": {
        "id": "microservice",
        "createdAt": "2016-09-14"
    }
}

RWAPIMicroservicePython.CT_URL = 'http://ct-url.com'


@pytest.fixture
def client():
    app = arcgis_proxy.app
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


@requests_mock.Mocker(kw='mocker')
def test_compute_histograms_without_rendering_rule(client, mocker):
    get_user_data_calls = mocker.get('http://ct-url.com/auth/user/me', status_code=200,
                                     json=json.dumps(USERS['MICROSERVICE']))

    response = client.get('/api/v1/arcgis-proxy/ImageServer/computeHistograms',
                          headers={'Authorization': 'Bearer abcd'})
    assert response.data == b'{"errors":[{"detail":"Must provide a valid renderingRule","status":400}]}\n'
    assert response.status_code == 400
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1


@requests_mock.Mocker(kw='mocker')
def test_compute_histograms_without_geostore_id(client, mocker):
    get_user_data_calls = mocker.get('http://ct-url.com/auth/user/me', status_code=200,
                                     json=json.dumps(USERS['MICROSERVICE']))

    response = client.get(
        '/api/v1/arcgis-proxy/ImageServer/computeHistograms?renderingRule={}'.format(json.dumps({})),
        headers={'Authorization': 'Bearer abcd'})
    assert response.data == b'{"errors":[{"detail":"Must provide a valid geostore ID","status":400}]}\n'
    assert response.status_code == 400
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1


@requests_mock.Mocker(kw='mocker')
def test_compute_histograms_without_server_url(client, mocker):
    get_user_data_calls = mocker.get('http://ct-url.com/auth/user/me', status_code=200,
                                     json=json.dumps(USERS['MICROSERVICE']))

    response = client.get(
        '/api/v1/arcgis-proxy/ImageServer/computeHistograms?renderingRule={}&geostore=1234'.format(json.dumps({})),
        headers={'Authorization': 'Bearer abcd'})
    assert response.data == b'{"errors":[{"detail":"either server or serverUrl is required","status":400}]}\n'
    assert response.status_code == 400
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1


@requests_mock.Mocker(kw='mocker')
def test_compute_histograms_without_service(client, mocker):
    get_user_data_calls = mocker.get('http://ct-url.com/auth/user/me', status_code=200,
                                     json=json.dumps(USERS['MICROSERVICE']))

    response = client.get(
        '/api/v1/arcgis-proxy/ImageServer/computeHistograms?renderingRule={}&geostore=1234&serverUrl=http://google.com'.format(
            json.dumps(json.dumps({}))), headers={'Authorization': 'Bearer abcd'})
    assert response.data == b'{"errors":[{"detail":"service is required","status":400}]}\n'
    assert response.status_code == 400
    assert get_user_data_calls.called
    assert get_user_data_calls.call_count == 1

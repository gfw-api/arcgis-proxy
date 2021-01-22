import json

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


@pytest.fixture
def client():
    app = arcgis_proxy.app
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


@requests_mock.Mocker(kw='mocker')
def test_compute_histograms_without_rendering_rule(client, mocker):
    response = client.get(
        '/api/v1/arcgis-proxy/ImageServer/computeHistograms?loggedUser={}'.format(json.dumps(USERS['MICROSERVICE'])))
    assert response.data == b'{"errors":[{"detail":"Must provide a valid renderingRule","status":400}]}\n'
    assert response.status_code == 400


@requests_mock.Mocker(kw='mocker')
def test_compute_histograms_without_geostore_id(client, mocker):
    response = client.get(
        '/api/v1/arcgis-proxy/ImageServer/computeHistograms?loggedUser={}&renderingRule={}'.format(json.dumps(USERS['MICROSERVICE']), json.dumps({})))
    assert response.data == b'{"errors":[{"detail":"Must provide a valid geostore ID","status":400}]}\n'
    assert response.status_code == 400


@requests_mock.Mocker(kw='mocker')
def test_compute_histograms_without_server_url(client, mocker):
    response = client.get(
        '/api/v1/arcgis-proxy/ImageServer/computeHistograms?loggedUser={}&renderingRule={}&geostore=1234'.format(json.dumps(USERS['MICROSERVICE']), json.dumps({})))
    assert response.data == b'{"errors":[{"detail":"either server or serverUrl is required","status":400}]}\n'
    assert response.status_code == 400


@requests_mock.Mocker(kw='mocker')
def test_compute_histograms_without_service(client, mocker):
    response = client.get(
        '/api/v1/arcgis-proxy/ImageServer/computeHistograms?loggedUser={}&renderingRule={}&geostore=1234&serverUrl=http://google.com'.format(json.dumps(USERS['MICROSERVICE']), json.dumps({})))
    assert response.data == b'{"errors":[{"detail":"service is required","status":400}]}\n'
    assert response.status_code == 400

import json
import os
import re

import requests_mock
from RWAPIMicroservicePython.test_utils import mock_request_validation

from arcgis_proxy.config.servers import servers
from arcgis_proxy import logging

from tests.fixtures.image_service_meta import image_service_meta
from tests.mocks import mock_geostore


histogram_route = "/api/v1/arcgis-proxy/ImageServer/computeHistograms"
geostore_id = "204c6ff1dae38a10953b19d452921283"

with open("tests/fixtures/histogram.json") as src:
    server_response = json.load(src)

with open("tests/fixtures/esrijson.json") as src:
    esrijson = json.load(src)

with open("tests/fixtures/esrijson_wm.json") as src:
    esrijson_wm = json.load(src)

with open("tests/fixtures/rendering_rule.json") as src:
    rendering_rule = json.load(src)

server_request = "https://gis-gfw.wri.org/arcgis/rest/services/image_services/analysis/ImageServer/computeHistograms"


def compose_query_params_histograms(
    server="gfw",
    service="image_services/analysis",
    rendering_rule=json.dumps(rendering_rule),
    mosaic_rule=None,
    pixel_size=100,
    geostore_id=geostore_id,
):
    """compose query parameter for ImageServer/computeHistograms endpoint"""

    if mosaic_rule is None:
        mosaic_rule = ""

    query_params = "?server={}&service={}&renderingRule={}&mosaicRule={}&pixelSize={}&geostore={}".format(
        server, service, rendering_rule, mosaic_rule, pixel_size, geostore_id
    )
    return query_params


@requests_mock.Mocker(kw="mocker")
def test_image_router_compute_histograms_no_server(client, mocker):
    """using false rendering rule"""

    logging.debug("[TEST]: Test compute histograms no server")

    server = ""
    query_params = compose_query_params_histograms(server=server)
    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))

    response = client.get(
        f"{histogram_route}{query_params}", headers={"x-api-key": "api-key-test"}
    )
    assert response.status_code == 400
    assert (
        response.json["errors"][0]["detail"] == "either server or serverUrl is required"
    )


@requests_mock.Mocker(kw="mocker")
def test_image_router_compute_histograms_false_server(client, mocker):
    """using false rendering rule"""

    logging.debug("[TEST]: Test compute histograms false server")

    server = "false-server"
    query_params = compose_query_params_histograms(server=server)
    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))

    response = client.get(
        f"{histogram_route}{query_params}", headers={"x-api-key": "api-key-test"}
    )
    assert response.status_code == 400
    assert (
        response.json["errors"][0]["detail"] == f"server not in list {servers.keys()}"
    )


@requests_mock.Mocker(kw="mocker")
def test_image_router_compute_histograms_no_service(client, mocker):
    """using false rendering rule"""

    logging.debug("[TEST]: Test compute histograms no service")

    service = ""
    query_params = compose_query_params_histograms(service=service)
    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))

    response = client.get(
        f"{histogram_route}{query_params}", headers={"x-api-key": "api-key-test"}
    )
    assert response.status_code == 400
    assert response.json["errors"][0]["detail"] == "service is required"


@requests_mock.Mocker(kw="mocker")
def test_image_router_compute_histograms_false_rendering_rule(client, mocker):
    """using false rendering rule"""

    logging.debug("[TEST]: Test compute histograms false rendering rule")

    rendering_rule = "False rule"
    query_params = compose_query_params_histograms(rendering_rule=rendering_rule)

    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))
    response = client.get(
        f"{histogram_route}{query_params}", headers={"x-api-key": "api-key-test"}
    )
    assert response.status_code == 400
    assert response.json["errors"][0]["detail"] == "renderingRule not a valid JSON"


@requests_mock.Mocker(kw="mocker")
def test_image_router_compute_histograms_false_mosaic_rule(client, mocker):
    """using false mosaic rule"""

    logging.debug("[TEST]: Test compute histograms false mosaic rule")

    mosaic_rule = "False rule"
    query_params = compose_query_params_histograms(mosaic_rule=mosaic_rule)

    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))
    response = client.get(
        f"{histogram_route}{query_params}", headers={"x-api-key": "api-key-test"}
    )
    assert response.status_code == 400
    assert response.json["errors"][0]["detail"] == "mosaicRule not a valid JSON"


@requests_mock.Mocker(kw="mocker")
def test_image_router_compute_histograms_no_rendering_rule(client, mocker):
    """using no rendering rule"""

    logging.debug("[TEST]: Test compute histograms no rendering rule")

    rendering_rule = ""
    query_params = compose_query_params_histograms(rendering_rule=rendering_rule)

    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))
    response = client.get(
        f"{histogram_route}{query_params}", headers={"x-api-key": "api-key-test"}
    )
    assert response.status_code == 400
    assert response.json["errors"][0]["detail"] == "Must provide a valid renderingRule"


@requests_mock.Mocker(kw="mocker")
def test_image_router_compute_histograms_false_pixel_size(client, mocker):
    """using false pixel size"""

    logging.debug("[TEST]: Test compute histograms false pixel size")

    pixel_size = "One"
    query_params = compose_query_params_histograms(pixel_size=pixel_size)

    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))
    response = client.get(
        f"{histogram_route}{query_params}", headers={"x-api-key": "api-key-test"}
    )
    assert response.status_code == 400
    assert response.json["errors"][0]["detail"] == "pixelSize must be of Type Integer"


@requests_mock.Mocker(kw="mocker")
def test_image_router_compute_histograms(client, mocker):
    """
    actual call to compute histogram using correct params
    expecting Image Server response

    """
    logging.debug("[TEST]: Test compute histograms")

    query_params = compose_query_params_histograms()

    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))
    mock_geostore(mocker)

    mocker.get(re.compile(".*gis.*"), status_code=200, json=image_service_meta)

    server_post_mock = mocker.post(re.compile(".*gis.*"), json=server_response)

    mock_request_validation(mocker, microservice_token=os.getenv("MICROSERVICE_TOKEN"))
    response = client.get(
        f"{histogram_route}{query_params}", headers={"x-api-key": "api-key-test"}
    )

    assert response.json == server_response
    assert str(esrijson_wm["rings"]) in str(server_post_mock.last_request.body)
    assert "esriGeometryPolygon" in str(server_post_mock.last_request.body)
    assert str(json.dumps(rendering_rule)) in str(server_post_mock.last_request.body)

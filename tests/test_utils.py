import json
import logging

import requests_mock

from arcgis_proxy.utils.reproject import reproject_esrijson
from arcgis_proxy.utils.services import get_image_service_url
from arcgis_proxy.utils.geostore import get_esrijson_wm
from arcgis_proxy.utils.geostore import get_geostore

from tests.mocks import mock_geostore


with open("tests/fixtures/geojson.json") as src:
    geojson = json.load(src)

with open("tests/fixtures/esrijson.json") as src:
    esrijson = json.load(src)

with open("tests/fixtures/esrijson_wm.json") as src:
    esrijson_wm = json.load(src)

with open("tests/fixtures/geostore.json") as src:
    geostore = json.load(src)

geostore_id = "204c6ff1dae38a10953b19d452921283"
service_url = "https://gis.forest-atlas.org/server/rest/services/eth/EthiopiaRestoration/ImageServer"


@requests_mock.Mocker(kw="mocker")
def test_get_geostore(client, mocker):
    """Test to make calls to geostore"""

    logging.debug("[TEST]: Test to make call to geostore")

    with client:
        mocked = mock_geostore(mocker)
        result = get_geostore(geostore_id, "api-key-test")

    assert result == geostore
    assert (
        f"/v1/geostore/{geostore_id}?format=esri"
        in f"{mocked.last_request.path}?{mocked.last_request.query}"
    )


# @mock.patch("arcgis_proxy.utils.geostore.get_geostore", side_effect=mocked_get_geostore)
@requests_mock.Mocker(kw="mocker")
def test_get_esrijson_wm(client, mocker):
    """Test to get ESRIJSON from geostore"""

    logging.debug("[TEST]: Test get ESRIJSON in WM from geostore")

    with client:
        mock_geostore(mocker)
        ej = get_esrijson_wm(geostore_id, "api-key-test")

    logging.debug("[TEST]: esrijson_wm: {}".format(esrijson_wm))

    assert ej == esrijson_wm
    # self.assertIn(mock.call(geostore_id), mock_geostore_id.call_args_list)


def test_reproject_esrijson():
    """Test if ESRI Json gets correctly projected into Web Mercator"""

    logging.debug("[TEST]: Test reproject ESRIJSON")

    esrijson_proj = reproject_esrijson(esrijson)
    assert esrijson_proj == esrijson_wm


def test_get_image_service_url():
    """Test if service URL gets correctly generated"""

    logging.debug("[TEST]: Test service URL generation")

    url = get_image_service_url(
        server="forest-atlas", service="eth/EthiopiaRestoration"
    )
    assert url == service_url

    url = get_image_service_url(
        server="forest-atlas", service="eth/EthiopiaRestoration"
    )
    assert url == service_url

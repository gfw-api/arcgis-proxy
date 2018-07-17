import unittest
import json
from arcgis_proxy import app
from arcgis_proxy.utils.reproject import reproject_esrijson
from arcgis_proxy.utils.services import get_image_service_url
import logging
from arcgis_proxy.config.servers import servers

with open('arcgis_proxy/tests/fixtures/geojson.json') as src:
    geojson = json.load(src)

with open('arcgis_proxy/tests/fixtures/esrijson.json') as src:
    esrijson = json.load(src)

with open('arcgis_proxy/tests/fixtures/esrijson_wm.json') as src:
    esrijson_wm = json.load(src)

with open('arcgis_proxy/tests/fixtures/histogram.json') as src:
    histogram = json.load(src)

geostore_id = "204c6ff1dae38a10953b19d452921283"
service_url = 'https://gis.forest-atlas.org/server/rest/services/eth/EthiopiaRestoration/ImageServer'


class UtilsTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_geostore(self):
        pass

    def test_get_esrijson_wm(self):
        pass

    def test_reproject_esrijson(self):

        # Test if ESRI Json gets correctly projected into Web Mercator

        logging.debug('[TEST]: Test reproject ESRIJSON')

        esrijson_proj = reproject_esrijson(esrijson)
        self.assertEqual(esrijson_proj, esrijson_wm)

    def test_get_image_service_url(self):

        # Test if service URL gets correctly generated

        logging.debug('[TEST]: Test service URL generation')

        url = get_image_service_url(server='forest-atlas', service='eth/EthiopiaRestoration')
        self.assertEquals(url, service_url)

        url = get_image_service_url(server='forest-atlas', service='eth/EthiopiaRestoration')
        self.assertEquals(url, service_url)


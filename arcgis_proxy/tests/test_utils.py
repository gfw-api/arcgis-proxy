import unittest
from unittest import mock
import json
from arcgis_proxy import app
from arcgis_proxy.utils.reproject import reproject_esrijson
from arcgis_proxy.utils.services import get_image_service_url
from arcgis_proxy.utils.geostore import get_esrijson_wm
from arcgis_proxy.utils.geostore import get_geostore

import logging
from arcgis_proxy.config.servers import servers

with open('arcgis_proxy/tests/fixtures/geojson.json') as src:
    geojson = json.load(src)

with open('arcgis_proxy/tests/fixtures/esrijson.json') as src:
    esrijson = json.load(src)

with open('arcgis_proxy/tests/fixtures/esrijson_wm.json') as src:
    esrijson_wm = json.load(src)

with open('arcgis_proxy/tests/fixtures/geostore.json') as src:
    geostore = json.load(src)

with open('arcgis_proxy/tests/fixtures/histogram.json') as src:
    histogram = json.load(src)

geostore_id = "204c6ff1dae38a10953b19d452921283"
service_url = 'https://gis.forest-atlas.org/server/rest/services/eth/EthiopiaRestoration/ImageServer'


def mocked_get_geostore(*args, **kwargs):

    # mock the get_geostore function so that we don't need geostore to be up during testing

    logging.debug('[MOCK]: args: {}'.format(args))
    if args[0] == geostore_id:
        return geostore
    else:
        return None


class UtilsTest(unittest.TestCase):

    # Test class for utils module

    def setUp(self):
        app.testing = True
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_geostore(self):
        pass

    @mock.patch('arcgis_proxy.utils.geostore.get_geostore', side_effect=mocked_get_geostore)
    def test_get_esrijson_wm(self, mock_gestore_id):

        # Test to get ESRIJSON from geostore

        logging.debug('[TEST]: Test get ESRIJSON in WM from geostore')

        ej = get_esrijson_wm(geostore_id)
        self.assertEqual(ej, esrijson_wm)

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


import unittest
import json
from arcgis_proxy import app
from arcgis_proxy.utils.reproject import reproject_esrijson
import logging


geojson = {"features": [{"properties": None, "type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[38, 10.4], [38.2, 10.4], [38.2, 10.2], [38, 10.2], [38, 10.4]]]}}], "crs": {}, "type": "FeatureCollection"}
esrijson = {"rings": [[[38, 10.4], [38.2, 10.4], [38.2, 10.2], [38, 10.2], [38, 10.4]]], "spatialReference": {"wkid": 4326}}
esrijson_wm = {'type': 'polygon', 'rings': [[[4230140.650144396, 1164132.904452777], [4252404.548303052, 1164132.904452777], [4252404.548303052, 1141504.3357174317], [4230140.650144396, 1141504.3357174317], [4230140.650144396, 1164132.904452777]]], '_ring': 0, 'spatialReference': {'wkid': 102100, 'latestWkid': 3857}}
geostore_id = "204c6ff1dae38a10953b19d452921283"
histogram = {"histograms": [{"counts": [0, 282, 0, 1586, 2795, 6062, 0, 4904, 4946, 2046, 25749, 17, 0, 0, 52, 0, 8], "max": 16.5, "min": -0.5, "size": 17}]}

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
        pass

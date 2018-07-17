import unittest
import json
from arcgis_proxy import app
from arcgis_proxy.config.servers import servers
from unittest import mock
from arcgis_proxy.routes.api.v1.image_router import compute_histograms
import logging


histogram_route = '/api/v1/arcgis-proxy/ImageServer/computeHistograms'
geostore_id = '204c6ff1dae38a10953b19d452921283'
server_response = {"histograms": [{"counts": [0, 282, 0, 1586, 2795, 6062, 0, 4904, 4946, 2046, 25749, 17, 0, 0, 52, 0, 8], "max": 16.5, "min": -0.5, "size": 17}]}
esri_json = {'type': 'polygon', 'rings': [[[4230140.650144396, 1164132.904452777], [4252404.548303052, 1164132.904452777], [4252404.548303052, 1141504.3357174317], [4230140.650144396, 1141504.3357174317], [4230140.650144396, 1164132.904452777]]], '_ring': 0, 'spatialReference': {'wkid': 102100, 'latestWkid': 3857}}
server_request = 'https://gis.forest-atlas.org/server/rest/services/eth/EthiopiaRestoration/ImageServer/computeHistograms'
rendering_rule = '{"rasterFunction":"Arithmetic","rasterFunctionArguments":{"Raster":"$1","Raster2":"$6","Operation":3}}'


def compose_query_params_histograms(server='forest-atlas',
                                    service='eth/EthiopiaRestoration',
                                    rendering_rule= rendering_rule,
                                    pixel_size=100,
                                    geostore_id=geostore_id):

    # compose query parameter for ImageServer/computeHistograms endpoint

    query_params = '?server={}&service={}&renderingRule={}&pixelSize={}&geostore={}'.format(
        server,
        service,
        rendering_rule,
        pixel_size,
        geostore_id)
    return query_params


def deserialize(response):

    # deserialize response and look for errors

    deserialized_response = json.loads(response.data)
    if 'errors' in deserialized_response.keys():
        data = None
        errors = deserialized_response['errors'][0]['detail']
    else:
        data = deserialized_response
        errors = None

    return data, errors


# This method will be used by the mock to replace requests.post to ImageServer
def mocked_requests_post(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
            self.text = json_data

        def json(self):
            return self.json_data

    if args[0] == server_request:
        return MockResponse(server_response, 200)
    else:
        return MockResponse(None, 404)


def mocked_get_esrijson_wm(*args, **kwargs):

    return esri_json


class ImageServiceHistogramTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def make_request(self, request, error=False):

        # make request to provided URL
        # if requests is suppose to fail assert status code 400
        # otherwise assert for status code 200

        response = self.app.get(request, follow_redirects=True)

        data, errors = deserialize(response)
        status_code = response.status_code

        if error:
            self.assertEqual(status_code, 400)
            return data, errors

        else:
            self.assertEqual(status_code, 200)
            return data, errors

    def test_image_router_compute_histograms_no_server(self):

        # using false rendering rule
        logging.debug('[TEST]: Test compute histograms no server')

        server = ""
        query_params = compose_query_params_histograms(server=server)
        data, errors = self.make_request('{}{}'.format(histogram_route, query_params), error=True)

        self.assertEqual(errors, 'either server or serverUrl is required')

    def test_image_router_compute_histograms_false_server(self):

        # using false rendering rule
        logging.debug('[TEST]: Test compute histograms false server')

        server = "false-server"
        query_params = compose_query_params_histograms(server=server)
        data, errors = self.make_request('{}{}'.format(histogram_route, query_params), error=True)

        self.assertEqual(errors, 'server not in list {}'.format(servers.keys()))

    def test_image_router_compute_histograms_no_service(self):

        # using false rendering rule
        logging.debug('[TEST]: Test compute histograms no service')

        service = ""
        query_params = compose_query_params_histograms(service=service)
        data, errors = self.make_request('{}{}'.format(histogram_route, query_params), error=True)

        self.assertEqual(errors, 'service is required')

    def test_image_router_compute_histograms_false_rendering_rule(self):

        # using false rendering rule
        logging.debug('[TEST]: Test compute histograms false rendering rule')

        rendering_rule = "False rule"
        query_params = compose_query_params_histograms(rendering_rule=rendering_rule)
        data, errors = self.make_request('{}{}'.format(histogram_route, query_params), error=True)

        self.assertEqual(errors, 'renderingRule not a valid JSON')

    def test_image_router_compute_histograms_no_rendering_rule(self):

        # using no rendering rule
        logging.debug('[TEST]: Test compute histograms no rendering rule')

        rendering_rule = ''
        query_params = compose_query_params_histograms(rendering_rule=rendering_rule)
        data, errors = self.make_request('{}{}'.format(histogram_route, query_params), error=True)

        self.assertEqual(errors, 'Must provide a valid renderingRule')

    def test_image_router_compute_histograms_false_pixel_size(self):

        # using false pixel size
        logging.debug('[TEST]: Test compute histograms false pixel size')

        pixel_size = "One"
        query_params = compose_query_params_histograms(pixel_size=pixel_size)
        data, errors = self.make_request('{}{}'.format(histogram_route, query_params), error=True)

        self.assertEqual(errors, 'pixelSize must be of Type Integer')

    @mock.patch('arcgis_proxy.routes.api.v1.image_router.requests.post', side_effect=mocked_requests_post)
    @mock.patch('arcgis_proxy.routes.api.v1.image_router.get_esrijson_wm', side_effect=mocked_get_esrijson_wm)
    def test_image_router_compute_histograms(self, mock_geostore, mock_post):

        logging.debug('[TEST]: Test compute histograms')

        query_params = compose_query_params_histograms()
        with app.test_request_context(path='{}{}'.format(histogram_route, query_params)):
            ch = compute_histograms()
            logging.debug('[TEST]: response:{}'.format(json.loads(ch[0].data)))
            self.assertEqual(json.loads(ch[0].data), server_response)

            logging.debug('[TEST]: POST {}'.format(mock_post.call_args_list))
            self.assertIn(mock.call(server_request,
                                    files={'geometry': (None, json.dumps(esri_json)),
                                           'geometryType': (None, 'esriGeometryPolygon'),
                                           'renderingRule': (None, json.dumps(rendering_rule)),
                                           'pixelSize': (None, '100'),
                                           'f': (None, 'json')}), mock_post.call_args_list)


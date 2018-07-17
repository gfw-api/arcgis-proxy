import unittest
import json
from arcgis_proxy import app
import requests
from httmock import all_requests, response, HTTMock, urlmatch


#@all_requests
#def response_content(url, request):
#    headers = {'content-type': 'application/json'}
#    content = {'error': 'wrong url'}
#    return response(400, content, headers, None, 5, request)

server = 'https://gis.forest-atlas.org/server'
service = 'eth/EthiopiaRestoration'
service_url = '{}/rest/services/{}/ImageServer/computeHistograms'.format(server, service)
rendering_rule = '{"rasterFunction":"Arithmetic","rasterFunctionArguments":{"Raster":"$1","Raster2":"$6","Operation":3}})'
pixel_size = 100
geometry = ""
geometry_type = ""
f = 'json'

geostore_id = '204c6ff1dae38a10953b19d452921283'
geostore_geom = '{"data":{"type":"geoStore","id":"204c6ff1dae38a10953b19d452921283","attributes":{"geojson":{"features":[{"properties":null,"type":"Feature","geometry":{"type":"Polygon","coordinates":[[[38,10.4],[38.2,10.4],[38.2,10.2],[38,10.2],[38,10.4]]]}}],"crs":{},"type":"FeatureCollection"},"hash":"204c6ff1dae38a10953b19d452921283","provider":{},"areaHa":48769.30305091247,"bbox":[38,10.2,38.2,10.4],"lock":false,"info":{"use":{}}}}}'

query_params = '?renderingRule={}&pixelSixe={}&geometry={}&geometryType={}&format={}'.format(rendering_rule,
                                                                                              pixel_size,
                                                                                              geometry,
                                                                                              geometry_type,
                                                                                              f)
histogram_route = '/api/v1/arcgis-proxy/ImageServer/computeHistograms'
server_request = r'{}{}'.format(service_url,query_params)
server_response =  {}


@urlmatch(netloc=server_request)
def image_server_mock(url, request):
    return server_response


class ParamsTest(unittest.TestCase):

    def setUp(self):
        app.testing = True
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def deserialize_error(self, response):
        return json.loads(response.data)['errors'][0]['detail']

    def make_false_request(self, request):
        response = self.app.get(request, follow_redirects=True)
        error = self.deserialize_error(response)
        status_code = response.status_code

        self.assertEqual(status_code, 400)

        return error

    def deserialize(self, response):
        return json.loads(response.data)

    def test_get_geostore(self):
        pass

    def test_get_esrijson_wm(self):
        pass

    def test_reproject_esrijson(self):
        pass

    def test_get_image_service_url(self):
        pass

    def test_image_router_compute_histograms_server(self):
        pass

    def test_image_router_compute_histograms_service(self):
        pass

    def test_image_router_compute_histograms_false_rendering_rule(self):
        rendering_rule = "False rule"
        query_params = '?server={}&service{}&renderingRule={}&pixelSixe={}&geostore={}'.format(
                                                                                        server,
                                                                                        service,
                                                                                        rendering_rule,
                                                                                        pixel_size,
                                                                                        geostore_id)
        response = self.app.get('{}{}'.format(histogram_route, query_params), follow_redirects=True)

        status_code = response.status_code
        self.assertEqual(status_code, 400)

        data = self.deserialize(response)
        self.assertEqual(data.get('errors')[0]['detail'], 'renderingRule not a valid JSON')

    def test_image_router_compute_histograms_no_rendering_rule(self):
        rendering_rule = ''
        query_params = '?server={}&service{}&renderingRule={}&pixelSixe={}&geostore={}'.format(
                                                                                        server,
                                                                                        service,
                                                                                        rendering_rule,
                                                                                        pixel_size,
                                                                                        geostore_id)
        response = self.app.get('{}{}'.format(histogram_route, query_params), follow_redirects=True)

        status_code = response.status_code
        self.assertEqual(status_code, 400)
        data = self.deserialize(response)
        self.assertEqual(data.get('errors')[0]['detail'], 'renderingRule not a valid JSON')

    def test_image_router_compute_histograms_false_pixel_size(self):
        pixel_size = "One"
        query_params = '?server={}&service{}&renderingRule={}&pixelSixe={}&geostore={}'.format(
                                                                                        server,
                                                                                        service,
                                                                                        rendering_rule,
                                                                                        pixel_size,
                                                                                        geostore_id)
        response = self.app.get('{}{}'.format(histogram_route, query_params), follow_redirects=True)

        status_code = response.status_code
        self.assertEqual(status_code, 400)

        data = self.deserialize(response)
        self.assertEqual(data.get('errors')[0]['detail'], 'pixelSize must be of Type Integer')

    def test_image_router_compute_histograms(self):
        with HTTMock(image_server_mock):
            query_params = '?server={}&service{}&renderingRule={}&pixelSixe={}&geostore={}'.format(
                                                                                            server,
                                                                                            service,
                                                                                            rendering_rule,
                                                                                            pixel_size,
                                                                                            geostore_id)
            response = self.app.get('{}{}'.format(histogram_route, query_params), follow_redirects=True)

            status_code = response.status_code
            self.assertEqual(status_code, 200)

            data = self.deserialize(response)

            for key in server_response.keys():
                self.assertEqual(data[0].get(key), server_response[key])

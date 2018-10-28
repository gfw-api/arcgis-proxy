from arcgis_proxy.config.servers import servers
import requests
import os
from arcgis_proxy.routes.api import error


def get_image_service_url(server=None, server_url=None, service=None):

    """ Generate Image Service URL based on server URL and service name """

    if server is not None:
        server_url = servers[server]

    return server_url + '/rest/services/' + service + '/ImageServer'


def get_feature_service_url(server=None, server_url=None, service=None, layer_id=None):

    """ Generate Feature Service URL based on server URL and service name """

    if server is not None:
        server_url = servers[server]

    service_url = server_url + '/rest/services/' + os.path.dirname(service)
    r = requests.get(service_url + "?f=pjson")

    if r.status_code == 200 or "error" in r.json().keys():
        services = r.json()["services"]
        for s in services:
            if s['name'] == service:
                if s['type'] == 'MapServer' or s['type'] == "FeatureServer":
                    return server_url + '/rest/services/' + service + '/' + s['type'] + '/' + layer_id

        return error(status=400, detail="Service not found or not a Feature/ MapServer")
    # Wrong status code
    return error(status=400, detail="Invalid Feature/ MapServer URL")

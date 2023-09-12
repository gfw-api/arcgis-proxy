from RWAPIMicroservicePython import request_to_microservice
from arcgis_proxy.routes.api import error
from arcgis_proxy.utils.reproject import reproject_esrijson


def get_geostore(geostore_id, api_key, format='esri'):
    """ make request to geostore microservice for user given geostore ID """

    return request_to_microservice(
        uri=f'/v1/geostore/{geostore_id}?format={format}',
        method='GET',
        api_key=api_key
    )


def get_esrijson_wm(geostore_id, api_key):

    """ get esrijson from geostore and reproject is into webmercator """

    geostore = get_geostore(geostore_id, api_key)

    if "errors" in geostore.keys():
        return error(status=400, detail=geostore["errors"])
    else:
        esrijson = reproject_esrijson(geostore["data"]["attributes"]["esrijson"])

    return esrijson

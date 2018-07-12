from CTRegisterMicroserviceFlask import request_to_microservice
from arcgis_proxy.routes.api import error
from arcgis_proxy.utils.reproject import reproject_esrijson


def get_geostore(geostore_id, format='esri'):
    config = {
            'uri': '/geostore/{}?format={}'.format(geostore_id, format),
            'method': 'GET',
    }

    return request_to_microservice(config)


def get_esrijson_wm(geostore_id):

    geostore = get_geostore(geostore_id)

    if "errors" in geostore.keys():
        return error(status=400, detail=geostore["errors"])
    else:
        esrijson = reproject_esrijson(geostore["data"]["attributes"]["esrijson"])

    return esrijson

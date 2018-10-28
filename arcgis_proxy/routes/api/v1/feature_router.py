import logging
import json
import requests

from flask import jsonify, Blueprint, request
from arcgis_proxy.routes.api import error
from arcgis_proxy.validators import validate_featureserver
from arcgis_proxy.utils.services import get_feature_service_url
from arcgis_proxy.utils.geostore import get_esrijson_wm

feature_endpoints = Blueprint('feature_endpoints', __name__)


@feature_endpoints.route('/query', strict_slashes=False, methods=['GET'])
@validate_featureserver
def query():
    """
    FeatureServer/query Endpoint
    Make request to feature sever and return query result

    """

    logging.info('[ROUTER]: Forward request to ArcGIS Feature Server')

    server = request.args.get('server', None)
    service = request.args.get('service', None)
    server_url = request.args.get('serverUrl', None)
    layer_id = request.args.get('layerId', None)
    geostore_id = request.args.get('geostore', None)

    where = request.args.get('where', None)
    objectIds = request.args.get('objectIds', None)
    spatialRel = request.args.get('spatialRel', None)
    relationParam = request.args.get('relationParam', None)
    time = request.args.get('time', None)
    distance = request.args.get('distance', None)
    units = request.args.get('units', None)
    outFields = request.args.get('outFields', None)
    returnGeometry = request.args.get('returnGeometry', None)
    maxAllowableOffset = request.args.get('maxAllowableOffset', None)
    geometryPrecision = request.args.get('geometryPrecision', None)
    outSR = request.args.get('outSR', None)
    gdbVersion = request.args.get('gdbVersion', None)
    returnDistinctValues = request.args.get('returnDistinctValues', None)
    returnIdsOnly = request.args.get('returnIdsOnly', None)
    returnCountOnly = request.args.get('returnCountOnly', None)
    returnExtentOnly = request.args.get('returnExtentOnly', None)
    orderByFields = request.args.get('orderByFields', None)
    groupByFieldsForStatistics = request.args.get('groupByFieldsForStatistics', None)
    outStatistics = request.args.get('outStatistics', None)
    returnZ = request.args.get('returnZ', None)
    returnM = request.args.get('returnM', None)
    multipatchOption = request.args.get('multipatchOption', None)
    resultOffset = request.args.get('resultOffset', None)
    resultRecordCount = request.args.get('resultRecordCount', None)
    quantizationParameters = request.args.get('quantizationParameters', None)
    returnCentroid = request.args.get('returnCentroid', None)
    historicMoment = request.args.get('historicMoment', None)
    returnTrueCurves = request.args.get('returnTrueCurves', None)
    sqlFormat = request.args.get('sqlFormat', None)
    returnExceededLimitFeatures = request.args.get('returnExceededLimitFeatures', None)

    service_url = get_feature_service_url(server, server_url, service, layer_id)

    # ArcGIS Server request a multi part form
    # we have to send payload as files
    # values need to be tuples with the first value set to None

    payload = {
        "geometry": (None, json.dumps(get_esrijson_wm(geostore_id))),
        "geometryType": (None, "esriGeometryPolygon"),
        "f": (None, "json")
    }

    logging.debug('[ROUTER]: payload: {}'.format(payload))

    try:
        r = requests.post(service_url + "/query", files=payload)

        logging.info('[ROUTER]: FeatureServer response: {}'.format(r.text))
        if r.status_code == 200:
            return jsonify(r.json()), 200
        else:
            return error(status=r.status_code, detail=r.text)
    except:
        return error(status=400, detail='Not a valid request')


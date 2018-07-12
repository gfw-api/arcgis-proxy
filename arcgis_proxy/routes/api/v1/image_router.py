"""API ROUTER"""

import logging
import json
import requests

from flask import jsonify, Blueprint, request
from arcgis_proxy.routes.api import error
from arcgis_proxy.validators import validate_geostore, validate_imageserver, validate_pixel_size, validate_rendering_rule
from arcgis_proxy.utils.services import get_image_service_url
from arcgis_proxy.utils.geostore import get_esrijson_wm

image_endpoints = Blueprint('image_endpoints', __name__)


@image_endpoints.route('/computeHistograms', strict_slashes=False, methods=['GET'])
@validate_pixel_size
@validate_rendering_rule
@validate_imageserver
@validate_geostore
def compute_histograms():
    """Image Endpoint"""
    logging.info('[ROUTER]: Forward request to ArcGIS Image Server')

    server = request.args.get('server', None)
    service = request.args.get('service', None)
    server_url = request.args.get('serverUrl', None)
    rendering_rule = request.args.get('renderingRule', None)
    pixelSize = request.args.get('pixelSize', None)
    geostore_id = request.args.get('geostore', None)

    service_url = get_image_service_url(server, server_url, service)

    # ArcGIS Server request a multi part form
    # we have to send payload as files
    # values need to be tuples with the first value set to None

    payload = {
        "geometry": (None, json.dumps(get_esrijson_wm(geostore_id))),
        "geometryType": (None, "esriGeometryPolygon"),
        "renderingRule": (None, json.dumps(rendering_rule)),
        "pixelSize": (None, pixelSize),
        "f": (None, "json")
    }

    try:
        r = requests.post(service_url + "/computeHistograms", files=payload)

        logging.info('[ROUTER]: {}'.format(r.text))
        if r.status_code == 200:
            return jsonify(r.json()), 200
        else:
            return error(status=r.status_code, detail=r.text)
    except:
        return error(status=400, detail='Not a valid request')


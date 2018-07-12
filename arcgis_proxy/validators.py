"""VALIDATORS"""

from functools import wraps
from arcgis_proxy.routes.api import error
from flask import request
import requests
import json
import logging
from arcgis_proxy.config.servers import servers
from arcgis_proxy.utils.services import get_image_service_url


def validate_rendering_rule(func):
    """Validation"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        renderingRule = request.args.get('renderingRule', None)

        # must have a rendering rule and rule must be a valid JSON
        if renderingRule is not None:
            try:
                json.loads(renderingRule)
            except ValueError:
                return error(status=400, detail="renderingRule not a valid JSON")
        else:
            return error(status=400, detail="Must provide a valid renderingRule")

        return func(*args, **kwargs)

    return wrapper


def validate_pixel_size(func):
    """pixelSize must be an integer or empty"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        pixelSize = request.args.get('pixelSize', None)

        if pixelSize is not None:
            try:
                int(pixelSize)
            except ValueError:
                return error(status=400, detail="pixelSize must be of Type Integer")

        return func(*args, **kwargs)

    return wrapper


def validate_geostore(func):
    """must have a geostore ID"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        geostore = request.args.get('geostore', None)

        if geostore is None:
            return error(status=400, detail="Must provide a valid geostore ID")

        return func(*args, **kwargs)

    return wrapper


def validate_imageserver(func):
    """serviceUrl parameter must be a valid ArcGIS Image Server instance"""
    @wraps(func)
    def wrapper(*args, **kwargs):

        server = request.args.get('server', None)
        service = request.args.get('service', None)
        server_url = request.args.get('serverUrl', None)

        if server is not None and server not in servers.keys():
            return error(status=400, detail="server not in list {}".format(servers.keys()))

        if service is None:
            return error(status=400, detail="service is required")

        if server_url is None and server is None:
            return error(status=400, detail="either server or serverUrl is required")

        service_url = get_image_service_url(server, server_url, service)
        logging.info('[VALIDATOR]: service_url {} {} {} {}'.format(server, server_url, service, service_url))

        try:
            r = requests.get(service_url + "?f=pjson")
            if r.status_code == 200:
                if not (r.json()["serviceDataType"][:16] == 'esriImageService'):
                    return error(status=400, detail="Not a valid Image Service URL")
            else:
                return error(status=400, detail="Not a valid Image Service URL: {}".format(service_url))
        except:
            return error(status=400, detail="Not a valid Image Service URL: {}".format(service_url))

        return func(*args, **kwargs)
    return wrapper

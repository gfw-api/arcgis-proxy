"""VALIDATORS"""

from functools import wraps
from arcgis_proxy.routes.api import error
from flask import request
import requests
import json
import logging
from arcgis_proxy.config.servers import servers
from arcgis_proxy.utils.services import get_image_service_url


def _validate_rendering_rule(rendering_rule):
    """Validation"""

    # must have a rendering rule and rule must be a valid JSON

    # logging.debug('[VALIDATOR]: validate rendering rule: {}'.format(rendering_rule))

    if rendering_rule:
        try:
            json.loads(rendering_rule)
        except ValueError:
            return error(status=400, detail="renderingRule not a valid JSON")
    else:
        return error(status=400, detail="Must provide a valid renderingRule")


def _validate_mosaic_rule(mosaic_rule):
    """Validation"""

    # may have an optional mosaic rule. Rule must be a valid JSON

    # logging.debug('[VALIDATOR]: validate mosaic rule: {}'.format(mosaic_rule))

    if mosaic_rule:
        try:
            json.loads(mosaic_rule)
        except ValueError:
            return error(status=400, detail="mosaicRule not a valid JSON")
    else:
        pass


def _validate_pixel_size(pixel_size):
    """pixelSize must be an integer or empty"""

    # logging.debug('[VALIDATOR]: validate pixel size')

    if pixel_size:
        try:
            int(pixel_size)
        except ValueError:
            return error(status=400, detail="pixelSize must be of Type Integer")


def _validate_geostore(geostore):
    """must have a geostore ID"""

    # logging.debug('[VALIDATOR]: validate geostore')

    if not geostore:
        return error(status=400, detail="Must provide a valid geostore ID")


def _validate_server(server, server_url):
    """most provide server or serverUrl"""

    # logging.debug('[VALIDATOR]: validate server')

    if server and server not in servers.keys():
        return error(status=400, detail="server not in list {}".format(servers.keys()))

    # logging.debug('[VALIDATOR]: validate server url')

    if not server_url and not server:
        return error(status=400, detail="either server or serverUrl is required")


def _validate_service(service):
    """must provide service URI"""

    # logging.debug('[VALIDATOR]: validate service')

    if not service:
        return error(status=400, detail="service is required")


def validate_imageserver(func):
    """serviceUrl parameter must be a valid ArcGIS Image Server instance"""

    @wraps(func)
    def wrapper(*args, **kwargs):

        logging.info('[VALIDATOR]: validate image service')

        server = request.args.get('server', None)
        service = request.args.get('service', None)
        server_url = request.args.get('serverUrl', None)
        geostore = request.args.get('geostore', None)
        pixel_size = request.args.get('pixelSize', None)
        rendering_rule = request.args.get('renderingRule', None)
        mosaic_rule = request.args.get('mosaicRule', None)
        if mosaic_rule == '':
            mosaic_rule = None

        logging.debug('[VALIDATOR]: server = {}'.format(server))
        logging.debug('[VALIDATOR]: service = {}'.format(service))
        logging.debug('[VALIDATOR]: server_url = {}'.format(server_url))
        logging.debug('[VALIDATOR]: geostore = {}'.format(geostore))
        logging.debug('[VALIDATOR]: pixel_size = {}'.format(pixel_size))
        logging.debug('[VALIDATOR]: rendering_rule = {}'.format(rendering_rule))
        logging.debug('[VALIDATOR]: mosaic_rule = {}'.format(mosaic_rule))

        v = _validate_rendering_rule(rendering_rule)
        if v:
            logging.debug('[VALIDATOR]: {}'.format(json.loads(v[0].data)))
            return v

        v = _validate_mosaic_rule(mosaic_rule)
        if v:
            logging.debug('[VALIDATOR]: {}'.format(json.loads(v[0].data)))
            return v

        v = _validate_geostore(geostore)
        if v:
            logging.debug('[VALIDATOR]: {}'.format(json.loads(v[0].data)))
            return v

        v = _validate_pixel_size(pixel_size)
        if v:
            logging.debug('[VALIDATOR]: {}'.format(json.loads(v[0].data)))
            return v

        v = _validate_server(server, server_url)
        if v:
            logging.debug('[VALIDATOR]: {}'.format(json.loads(v[0].data)))
            return v

        v = _validate_service(service)
        if v:
            logging.debug('[VALIDATOR]: {}'.format(json.loads(v[0].data)))
            return v

        service_url = get_image_service_url(server, server_url, service)
        logging.debug('[VALIDATOR]: service_url {}'.format(service_url))

        try:
            r = requests.get(service_url + "?f=pjson")
            if r.status_code == 200:
                if not (r.json()["serviceDataType"][:16] == 'esriImageService'):
                    return error(status=400, detail="Not a valid Image Service URL")
            else:
                return error(status=400, detail="Not a valid Image Service URL")
        except Exception as e:
            return error(status=400, detail=e)

        return func(*args, **kwargs)

    return wrapper

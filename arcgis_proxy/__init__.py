"""The API MODULE"""

import os
import json
import logging

from flask import Flask
from arcgis_proxy.config import SETTINGS
from arcgis_proxy.routes.api import error
from arcgis_proxy.routes.api.v1 import image_endpoints, feature_endpoints
from arcgis_proxy.utils.files import load_config_json
import CTRegisterMicroserviceFlask

logging.basicConfig(
    level=SETTINGS.get('logging', {}).get('level'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)

# Flask App
app = Flask(__name__)

# Routing

app.register_blueprint(image_endpoints, url_prefix='/api/v1/arcgis-proxy/ImageServer')
app.register_blueprint(feature_endpoints, url_prefix='/api/v1/arcgis-proxy/FeatureServer')


# CT
info = load_config_json('register')
swagger = load_config_json('swagger')
CTRegisterMicroserviceFlask.register(
    app=app,
    name='arcgis_proxy',
    info=info,
    swagger=swagger,
    mode=CTRegisterMicroserviceFlask.AUTOREGISTER_MODE if os.getenv('CT_REGISTER_MODE') and os.getenv('CT_REGISTER_MODE') == 'auto' else CTRegisterMicroserviceFlask.NORMAL_MODE,
    ct_url=os.getenv('CT_URL'),
    url=os.getenv('LOCAL_URL')
)


@app.errorhandler(403)
def forbidden(e):
    return error(status=403, detail='Forbidden')


@app.errorhandler(404)
def page_not_found(e):
    return error(status=404, detail='Not Found')


@app.errorhandler(405)
def method_not_allowed(e):
    return error(status=405, detail='Method Not Allowed')


@app.errorhandler(410)
def gone(e):
    return error(status=410, detail='Gone')


@app.errorhandler(500)
def internal_server_error(e):
    return error(status=500, detail='Internal Server Error')

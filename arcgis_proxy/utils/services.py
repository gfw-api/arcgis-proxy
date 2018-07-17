from arcgis_proxy.config.servers import servers


def get_image_service_url(server=None, server_url=None, service=None):

    """ Generate Image Service URL based on server URL and service name """

    if server is not None:
        server_url = servers[server]

    return server_url + '/rest/services/' + service + '/ImageServer'

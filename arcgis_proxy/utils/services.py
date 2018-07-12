from arcgis_proxy.config.servers import servers


def get_image_service_url(server, server_url, service):

    if server is not None:
        server_url = servers[server]

    return server_url + '/rest/services/' + service + '/ImageServer'

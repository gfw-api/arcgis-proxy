import re


def mock_geostore(mocker):
    matcher = re.compile(".*/geostore.*")
    return mocker.get(
        matcher,
        request_headers={
            "x-api-key": "api-key-test",
        },
        status_code=200,
        json={
            "data": {
                "type": "geoStore",
                "id": "204c6ff1dae38a10953b19d452921283",
                "attributes": {
                    "geojson": {
                        "features": [
                            {
                                "properties": None,
                                "type": "Feature",
                                "geometry": {
                                    "type": "Polygon",
                                    "coordinates": [
                                        [
                                            [38, 10.4],
                                            [38.2, 10.4],
                                            [38.2, 10.2],
                                            [38, 10.2],
                                            [38, 10.4],
                                        ]
                                    ],
                                },
                            }
                        ],
                        "crs": {},
                        "type": "FeatureCollection",
                    },
                    "hash": "204c6ff1dae38a10953b19d452921283",
                    "provider": {},
                    "areaHa": 48769.30305091247,
                    "bbox": [38, 10.2, 38.2, 10.4],
                    "lock": False,
                    "esrijson": {
                        "rings": [
                            [
                                [38, 10.4],
                                [38.2, 10.4],
                                [38.2, 10.2],
                                [38, 10.2],
                                [38, 10.4],
                            ]
                        ],
                        "spatialReference": {"wkid": 4326},
                    },
                    "info": {"use": {}},
                },
            }
        },
    )

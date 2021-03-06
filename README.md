# Arcgis proxy microservice

[![Build Status](https://travis-ci.com/gfw-api/arcgis-proxy.svg?branch=dev)](https://travis-ci.com/gfw-api/arcgis-proxy)
[![Test Coverage](https://api.codeclimate.com/v1/badges/cccb3b1b648ce4686ca5/test_coverage)](https://codeclimate.com/github/gfw-api/arcgis-proxy/test_coverage)

Arcgis-proxy is a microservice for the GFW API. It allows making calls to ArcGIS Server using the GFW geostore.

The proxy fetches the geostore geometry, converts it ESRI JSON and projects it into Web  Mercator projections and forwards the call to ArcGIS server.
It returns the ArcGIS server response.

## Dependencies

Dependencies on other Microservices:

- [Geostore](https://github.com/gfw-api/gfw-geostore-api)

## Functionality

In its current version the proxy only supports calls to ImageServer service for the `computeHistorgrams` function

```
/v1/arcgis-proxy/ImageServer/computeHistograms
```

Parameters | Explanation | Data Type
-----------|--------------|----------
server | a known ArcGIS server instance (either gfw or forest-atlas) | string
serverUrl | URL to the ArcGIS Server instance (server web adaptor). Use either server or serverUrl | URL
service | the service name | String
renderingRule | the rendering rule | JSON
pixelSize | pixel size for calculation | integer
geostore | geostore ID | hash


Example
```
http://production-api.globalforestwatch.org//v1/arcgis-proxy/ImageServer/computeHistograms?server=forest-atlas&service=eth/EthiopiaRestoration&geostore=d1193c16181805c30701dea9a173e30b&renderingRule={"rasterFunction":"Arithmetic","rasterFunctionArguments":{"Raster":"$1","Raster2":"$6","Operation":3}}&pixelSize=100
```


## Tests

As this microservice relies on Google Earth Engine, tests require a valid `storage.json` or equivalent file. 
At the time of this writing, actual tests use mock calls, so the real credential are only needed because Google's 
library actually validates the credentials on startup. 

Before you run the tests, be sure to install the necessary development libraries, using `pip install -r requirements_dev.txt`.

Actual test execution is done by running the `pytest` executable on the root of the project.  

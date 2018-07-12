# arcgis-proxy

Arcgis-proxy is a micro service for the GFW API. It allows to make calls to ArcGIS Server using the GFW geostore.
The proxy fetches the geostore geometry, converts it ESRI JSON and projects it into Web  Mercator projections and forwards the call to ArcGIS server.
It returns the ArcGIS server response.

## Functionality

In its current version the proxy only supports calls to ImageServer service for the `computeHistorgrams` function

```
/v1/arcgis-proxy/ImageServer/computeHistograms
```

Parameters | Explaination | Data Type
-----------|--------------|----------
server | a known ArcGIS server instance (either gfw or forest-atlas) | string
serverUrl | URL to the ArcGIS Server instance (server web adaptor). Use either server or serverUrl | URL
service | the service name | String
renderingRule | the rendering rule | JSON
pixelSize | prixel size for calculation | integer
geostore | geostore ID | hash


Example
```
http://production-api.globalforestwatch.org//v1/arcgis-proxy/ImageServer/computeHistograms?server=forest-atlas&service=eth/EthiopiaRestoration&geostore=d1193c16181805c30701dea9a173e30b&renderingRule={"rasterFunction":"Arithmetic","rasterFunctionArguments":{"Raster":"$1","Raster2":"$6","Operation":3}}&pixelSize=100
```

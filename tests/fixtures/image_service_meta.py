image_service_meta = {
    "currentVersion": 10.61,
    "serviceDescription": "image_services/analysis",
    "name": "image_services/analysis",
    "description": "",
    "extent": {
        "xmin": -1.6921202422941137e7,
        "ymin": -8460600.961471582,
        "xmax": 1.6921202422941137e7,
        "ymax": 8460600.961471582,
        "spatialReference": {"wkid": 54012, "latestWkid": 54012},
    },
    "initialExtent": {
        "xmin": -1.6921202422941137e7,
        "ymin": -8460600.961471582,
        "xmax": 1.6921202422941137e7,
        "ymax": 8460600.961471582,
        "spatialReference": {"wkid": 54012, "latestWkid": 54012},
    },
    "fullExtent": {
        "xmin": -1.6921202422941137e7,
        "ymin": -8460600.961471582,
        "xmax": 1.6921202422941137e7,
        "ymax": 8460600.961471582,
        "spatialReference": {"wkid": 54012, "latestWkid": 54012},
    },
    "pixelSizeX": 4.999999977230087,
    "pixelSizeY": 4.9999990907689975,
    "bandCount": 1,
    "pixelType": "U16",
    "minPixelSize": 0,
    "maxPixelSize": 0,
    "copyrightText": "",
    "serviceDataType": "esriImageServiceDataTypeProcessed",
    "minValues": [0],
    "maxValues": [14],
    "meanValues": [1.725407490348532],
    "stdvValues": [3.5139908331619076],
    "objectIdField": "OBJECTID",
    "fields": [
        {
            "name": "OBJECTID",
            "type": "esriFieldTypeOID",
            "alias": "OBJECTID",
            "domain": None,
        },
        {
            "name": "Shape",
            "type": "esriFieldTypeGeometry",
            "alias": "Shape",
            "domain": None,
        },
        {
            "name": "Name",
            "type": "esriFieldTypeString",
            "alias": "Name",
            "domain": None,
            "length": 50,
        },
        {
            "name": "MinPS",
            "type": "esriFieldTypeDouble",
            "alias": "MinPS",
            "domain": None,
        },
        {
            "name": "MaxPS",
            "type": "esriFieldTypeDouble",
            "alias": "MaxPS",
            "domain": None,
        },
        {
            "name": "LowPS",
            "type": "esriFieldTypeDouble",
            "alias": "LowPS",
            "domain": None,
        },
        {
            "name": "HighPS",
            "type": "esriFieldTypeDouble",
            "alias": "HighPS",
            "domain": None,
        },
        {
            "name": "Category",
            "type": "esriFieldTypeInteger",
            "alias": "Category",
            "domain": {
                "type": "codedValue",
                "name": "MosaicCatalogItemCategoryDomain",
                "description": "Catalog item categories.",
                "codedValues": [
                    {"name": "Unknown", "code": 0},
                    {"name": "Primary", "code": 1},
                    {"name": "Overview", "code": 2},
                    {"name": "Unprocessed Overview", "code": 3},
                    {"name": "Partial Overview", "code": 4},
                    {"name": "Inactive", "code": 5},
                    {"name": "Uploaded", "code": 253},
                    {"name": "Incomplete", "code": 254},
                    {"name": "Custom", "code": 255},
                ],
                "mergePolicy": "esriMPTDefaultValue",
                "splitPolicy": "esriSPTDefaultValue",
            },
        },
        {
            "name": "Tag",
            "type": "esriFieldTypeString",
            "alias": "Tag",
            "domain": None,
            "length": 20,
        },
        {
            "name": "GroupName",
            "type": "esriFieldTypeString",
            "alias": "GroupName",
            "domain": None,
            "length": 50,
        },
        {
            "name": "ProductName",
            "type": "esriFieldTypeString",
            "alias": "ProductName",
            "domain": None,
            "length": 50,
        },
        {
            "name": "CenterX",
            "type": "esriFieldTypeDouble",
            "alias": "CenterX",
            "domain": None,
        },
        {
            "name": "CenterY",
            "type": "esriFieldTypeDouble",
            "alias": "CenterY",
            "domain": None,
        },
        {
            "name": "ZOrder",
            "type": "esriFieldTypeInteger",
            "alias": "ZOrder",
            "domain": None,
        },
        {
            "name": "Shape_Length",
            "type": "esriFieldTypeDouble",
            "alias": "Shape_Length",
            "domain": None,
        },
        {
            "name": "Shape_Area",
            "type": "esriFieldTypeDouble",
            "alias": "Shape_Area",
            "domain": None,
        },
    ],
    "capabilities": "Catalog,Mensuration,Image,Metadata",
    "defaultMosaicMethod": "Northwest",
    "allowedMosaicMethods": "NorthWest,Center,LockRaster,ByAttribute,Nadir,Viewpoint,Seamline,None",
    "sortField": "",
    "sortValue": None,
    "mosaicOperator": "First",
    "maxDownloadSizeLimit": 2048,
    "defaultCompressionQuality": 75,
    "defaultResamplingMethod": "Nearest",
    "maxImageHeight": 15000,
    "maxImageWidth": 15000,
    "maxRecordCount": 1000,
    "maxDownloadImageCount": 20,
    "maxMosaicImageCount": 20,
    "allowRasterFunction": True,
    "rasterFunctionInfos": [
        {"name": "None", "description": "A No-Op Function.", "help": ""}
    ],
    "rasterTypeInfos": [
        {
            "name": "Raster Dataset",
            "description": "Supports all ArcGIS Raster Datasets",
            "help": "",
        }
    ],
    "mensurationCapabilities": "Basic",
    "hasHistograms": True,
    "hasColormap": False,
    "hasRasterAttributeTable": False,
    "minScale": 0,
    "maxScale": 0,
    "exportTilesAllowed": False,
    "hasMultidimensions": False,
    "supportsStatistics": True,
    "supportsAdvancedQueries": True,
    "editFieldsInfo": None,
    "ownershipBasedAccessControlForRasters": None,
    "allowComputeTiePoints": False,
    "useStandardizedQueries": True,
    "advancedQueryCapabilities": {
        "useStandardizedQueries": True,
        "supportsStatistics": True,
        "supportsOrderBy": True,
        "supportsDistinct": True,
        "supportsPagination": True,
    },
    "spatialReference": {"wkid": 54012, "latestWkid": 54012},
}
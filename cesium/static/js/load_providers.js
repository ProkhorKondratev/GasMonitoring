function createUrlTemplateProvider(layer) {
    return new Cesium.UrlTemplateImageryProvider({
        url: layer.tileProvider.url,
        credit: layer.tileProvider.credit,
        minimumLevel: layer.tileProvider.minimumLevel,
        maximumLevel: layer.tileProvider.maximumLevel !== null ? layer.tileProvider.maximumLevel : undefined,
        tileHeight: layer.tileProvider.tileHeight,
        tileWidth: layer.tileProvider.tileWidth,
    });
}

function createSingleTileProvider(layer) {
    return new Cesium.SingleTileImageryProvider({
        url: layer.tileProvider.url,
        credit: layer.tileProvider.credit
    });
}

function createTerrainProvider(layer) {
    return new Cesium.CesiumTerrainProvider({
        url: layer.tileProvider.url,
        credit: layer.tileProvider.credit
    });
}

const imageryProviderTypeMap = {
    UrlTemplateImageryProvider: createUrlTemplateProvider,
    SingleTileImageryProvider: createSingleTileProvider
};

const terrainProviderTypeMap = {
    TerrainProvider: createTerrainProvider
};

async function fetchTileProviders(layers = null) {
    let responseData = layers;

    if (!layers || layers.length === 0) {
        try {
            const response = await fetch('/api/provider_views/');
            responseData = await response.json();
        } catch (error) {
            console.error(error);
            return;
        }
    }

    const imageryProviders = [];
    const terrainProviders = [];

    for (const layer of responseData) {
        if (layer.is_enabled) {
            const imageryProviderFactory = imageryProviderTypeMap[layer.tileProvider.type];
            const terrainProviderFactory = terrainProviderTypeMap[layer.tileProvider.type];

            const provider = new Cesium.ProviderViewModel({
                name: layer.name,
                tooltip: layer.tooltip,
                iconUrl: Cesium.buildModuleUrl(layer.iconUrl),
                category: layer.category,
                creationFunction: function () {
                    if (imageryProviderFactory) {
                        return imageryProviderFactory(layer);
                    } else if (terrainProviderFactory) {
                        return terrainProviderFactory(layer);
                    }
                }
            });

            if (imageryProviderFactory) {
                imageryProviders.push(provider);
            } else if (terrainProviderFactory) {
                terrainProviders.push(provider);
            }
        }
    }

    return {
        imageryProviders,
        terrainProviders
    };
}

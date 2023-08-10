async function setupCesium() {
    const viewer = await fetchViewer('cesiumContainer');

    const zones = await ApiService.getZMR();

    Cesium.GeoJsonDataSource.load(zones, {
        stroke: Cesium.Color.RED,
        fill: Cesium.Color.RED.withAlpha(0.3),
        strokeWidth: 3,
    }).then((dataSource) => {
        viewer.dataSources.add(dataSource)
        viewer.zoomTo(dataSource)
    })

}

setupCesium();

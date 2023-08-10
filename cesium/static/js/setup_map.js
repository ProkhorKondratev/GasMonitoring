async function setupCesium() {
    const viewer = await fetchViewer('cesiumContainer');

    viewer.entities.add({
        name: 'Cesium',
        position: Cesium.Cartesian3.fromDegrees(37.6178, 55.7517),
        point: {
            pixelSize: 10,
            color: Cesium.Color.RED,
            outlineColor: Cesium.Color.WHITE,
        }
    });

    viewer.zoomTo(viewer.entities);
}

setupCesium();

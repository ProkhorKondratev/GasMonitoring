async function setupCesium() {
    const viewer = await fetchViewer('cesiumContainer');

    function handleTileLoadProgress(progress) {
        if (progress === 1) {
            console.log('Карта загружена');
            viewer.scene.globe.tileLoadProgressEvent.removeEventListener(handleTileLoadProgress);
        }
    }

    viewer.scene.globe.tileLoadProgressEvent.addEventListener(handleTileLoadProgress);


    const zoneStyle = await fetchStyle('Polygon')
    const zones = await ApiService.getZMR();

    for (const zone of zones.features) {
        const zoneCoordinates = zone.geometry.coordinates.flat(Infinity)

        const zoneEntity = new Cesium.Entity({
            name: zone.properties.name,
            polygon: zoneStyle,
        })
        zoneEntity.polygon.hierarchy = Cesium.Cartesian3.fromDegreesArray(zoneCoordinates)

        viewer.entities.add(zoneEntity)
    }
    viewer.flyTo(viewer.entities)
}

setupCesium();

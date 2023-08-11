async function setupCesium() {
    const viewer = await fetchViewer('cesiumContainer');

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
    viewer.zoomTo(viewer.entities)
}

setupCesium();

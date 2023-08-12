class CesiumMap {
    constructor(containerId) {
        this.containerId = containerId;
        this.viewer = null;
        this.scene = null;

        this.objectManager = null
        this.styleManager = null
    }

    async init() {
        await this.setupCesium();

        this.styleManager = new StyleManager();
        await this.styleManager.init();

        this.objectManager = new ObjectManager(this.viewer, this.styleManager);
        await this.objectManager.init();
    }

    async setupCesium() {
        this.viewer = await fetchViewer(this.containerId);

        this.handleTileLoadProgress = this.handleTileLoadProgress.bind(this);
        this.viewer.scene.globe.tileLoadProgressEvent.addEventListener(this.handleTileLoadProgress);
    }

    handleTileLoadProgress(progress) {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (progress === 0) {
            // анимируем плавное исчезновение и в конце скрываем
            loadingOverlay.animate([{opacity: 1}, {opacity: 0}], {duration: 500}).onfinish = () => {
                loadingOverlay.style.display = 'none';
            }
            console.log('Карта загружена');
            this.viewer.scene.globe.tileLoadProgressEvent.removeEventListener(this.handleTileLoadProgress);
        } else {
            loadingOverlay.style.display = 'flex';
        }
    }
}

class StyleManager {
    constructor() {
        this.zoneBaseStyle = null;
        this.polylineBaseStyle = null;

    }

    async init() {
        await this.loadBaseStyles()
    }

    async loadBaseStyles() {
        this.zoneBaseStyle = await fetchStyle('Polygon');
        this.polylineBaseStyle = await fetchStyle('Polyline');
    }
}


class ObjectManager {
    constructor(viewer, styleManager) {
        this.viewer = viewer;
        this.styleManager = styleManager;

        this.zmr_source = null;
        this.selectedObjects = [];
    }

    async init() {
        this.zmr_source = new Cesium.CustomDataSource('zmr');
        await this.loadZMR();

        this.viewer.dataSources.add(this.zmr_source).then(
            () => {
                this.viewer.zoomTo(this.zmr_source.entities)
            }
        )
        this.leftClickOnObject(this.highlightObject)
    }

    async loadZMR() {
        const zones = await ApiService.getZMR();
        for (const zmr of zones.features) {
            const zoneCoordinates = zmr.geometry.coordinates.flat(Infinity)

            const zoneEntity = new Cesium.Entity({
                id: zmr.id,
                name: zmr.properties.name,
                polygon: this.styleManager.zoneBaseStyle,
                polyline: this.styleManager.polylineBaseStyle,
            })
            zoneEntity.polygon.hierarchy = Cesium.Cartesian3.fromDegreesArray(zoneCoordinates)
            zoneEntity.polyline.positions = Cesium.Cartesian3.fromDegreesArray(zoneCoordinates)
            this.zmr_source.entities.add(zoneEntity)
        }
    }

    leftClickOnObject(clickFunction = null) {
        this.viewer.screenSpaceEventHandler.setInputAction(movement => {
            const pickedObject = this.viewer.scene.pick(movement.position);
            if (Cesium.defined(pickedObject)) {
                console.log(`Выбран: ${pickedObject.id.name} (${pickedObject.id.id})`);

                if (clickFunction) {
                    const index = this.selectedObjects.indexOf(pickedObject.id);
                    if (index !== -1) {
                        this.selectedObjects.splice(index, 1); // Убираем объект из массива выбранных
                        this.clearSelection(pickedObject.id); // Снимаем выделение
                    } else {
                        this.selectedObjects.push(pickedObject.id);
                        clickFunction(pickedObject.id);
                    }
                }

                if (this.selectedObjects.length === 2) {
                    this.measureDistanceBetween();
                }

            } else {
                for (const object of this.selectedObjects) {
                    this.clearSelection(object);
                }
            }
        }, Cesium.ScreenSpaceEventType.LEFT_CLICK);
    }

    clearSelection(object) {
        if (object) {
            const object_geometry = object.polygon.hierarchy.getValue().positions

            object.polygon = this.styleManager.zoneBaseStyle;
            object.polyline = this.styleManager.polylineBaseStyle;

            object.polygon.hierarchy = object_geometry
            object.polyline.positions = object_geometry
        }
    }

    highlightObject(object) {
        object.polygon.material = Cesium.Color.RED.withAlpha(0.5);
        object.polyline.material = Cesium.Color.RED.withAlpha(0.5);
    }

    //TODO Оптимизировать, расширить функционал
    measureDistanceBetween() {
        const poly1Positions = this.selectedObjects[0].polygon.hierarchy.getValue().positions
        const poly2Positions = this.selectedObjects[1].polygon.hierarchy.getValue().positions

        let closestDistance = Number.MAX_VALUE;
        let closestPoint1, closestPoint2;

        for (let i = 0; i < poly1Positions.length; i++) {
            for (let j = 0; j < poly2Positions.length; j++) {
                let distance = Cesium.Cartesian3.distance(poly1Positions[i], poly2Positions[j]);
                if (distance < closestDistance) {
                    closestDistance = distance;
                    closestPoint1 = poly1Positions[i];
                    closestPoint2 = poly2Positions[j];
                }
            }
        }

        this.viewer.entities.add({
            position: closestPoint1,
            point: {
                pixelSize: 10,
                color: Cesium.Color.RED,
            }
        })

        this.viewer.entities.add({
            position: closestPoint2,
            point: {
                pixelSize: 10,
                color: Cesium.Color.RED,
            }
        })

        this.viewer.entities.add({
            polyline: {
                positions: [closestPoint1, closestPoint2],
                width: 5,
                material: Cesium.Color.RED,
            }
        })

        this.viewer.entities.add({
            position: Cesium.Cartesian3.midpoint(closestPoint1, closestPoint2, new Cesium.Cartesian3()),
            label: {
                text: `${Math.round(closestDistance / 1000)} км`,
                font: '12px sans-serif',
                fillColor: Cesium.Color.PURPLE,
                pixelOffset: new Cesium.Cartesian2(8, -10),
            }
        })
    }

}

const map = new CesiumMap('cesiumContainer')
map.init()

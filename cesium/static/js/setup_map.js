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
        this.viewer.extend(Cesium.viewerDragDropMixin);

        this.dataSourceAddedListener = this.handleDataSourceAdded.bind(this);
        this.viewer.dataSources.dataSourceAdded.addEventListener(this.dataSourceAddedListener);
    }

    handleDataSourceAdded(dataSourceCollection, dataSource) {
        const loadingOverlay = document.getElementById('loading-overlay');
        if (dataSource.name === 'protection_objects') {
            loadingOverlay.animate([{opacity: 1}, {opacity: 0}], {duration: 500}).onfinish = () => {
                loadingOverlay.style.display = 'none';
            }
            console.log('Карта загружена');

            this.viewer.dataSources.dataSourceAdded.removeEventListener(this.dataSourceAddedListener);
        } else {
            loadingOverlay.style.display = 'flex';
        }
    }
}

class StyleManager {
    async init() {
        await this.loadBaseStyles()
    }

    async loadBaseStyles() {
        this.zmrBaseStyle = await fetchStyle('Polygon', 1);
        this.zmrPolylineBaseStyle = await fetchStyle('Polyline', 2);

        this.ozBaseStyle = await fetchStyle('Polygon', 2);
        this.ozPolylineBaseStyle = await fetchStyle('Polyline', 3);

        this.tubeBaseStyle = await fetchStyle('Polyline', 4);
    }
}


class ObjectManager {
    constructor(viewer, styleManager) {
        this.viewer = viewer;
        this.styleManager = styleManager;

        this.selectedObjects = [];
    }

    async init() {
        this.loadProtectionZones();
        this.loadProtectionObjects();

        this.leftClickOnObject(this.highlightObject)
    }

    async loadProtectionZones() {
        const protectionZones = await ApiService.getProtectionZones();

        protectionZones.features.map(async (zone) => {
            const ds = new Cesium.GeoJsonDataSource(`protection_zones_${zone.id}`);

            this.viewer.dataSources.add(ds);
            await ds.load(zone);

            if (ds.entities.values.length === 2) {
                const [zmr, oz] = ds.entities.values;
                ds.entities.removeAll();

                const zmrPositions = zmr.polygon?.hierarchy.getValue()?.positions;
                const ozPositions = oz.polygon?.hierarchy.getValue()?.positions;

                if (zmrPositions && ozPositions) {
                    oz.polygon = this.styleManager.ozBaseStyle;
                    oz.polyline = this.styleManager.ozPolylineBaseStyle;
                    oz.polygon.hierarchy = ozPositions;
                    oz.polyline.positions = ozPositions;

                    const zonesHierarchy = {
                        positions: zmrPositions,
                        holes: [{positions: ozPositions}]
                    };

                    const zones = new Cesium.Entity({
                        id: `zmr_${zone.id}`,
                        name: zmr.name,
                        polygon: this.styleManager.zmrBaseStyle,
                        polyline: this.styleManager.zmrPolylineBaseStyle
                    });

                    zones.polygon.hierarchy = zonesHierarchy;
                    zones.polyline.positions = zmrPositions;

                    ds.entities.add(zones);
                    ds.entities.add(oz);
                }
            } else if (ds.entities.values.length > 2) {
                console.log('Получено больше 2-х объектов', zone.id);
                const entities = ds.entities.values;
                ds.entities.removeAll();

                for (let i = 0; i < entities.length; i += 2) {
                    const zmr = entities[i];
                    const oz = entities[i + 1];

                    const zmrPositions = zmr.polygon?.hierarchy.getValue()?.positions;
                    const ozPositions = oz.polygon?.hierarchy.getValue()?.positions;

                    if (zmrPositions && ozPositions) {
                        oz.polygon = this.styleManager.ozBaseStyle;
                        oz.polyline = this.styleManager.ozPolylineBaseStyle;
                        oz.polygon.hierarchy = ozPositions;
                        oz.polyline.positions = ozPositions;

                        const zonesHierarchy = {
                            positions: zmrPositions,
                            holes: [{positions: ozPositions}]
                        };

                        const zones = new Cesium.Entity({
                            id: `zmr_${zone.id}_${i}`,
                            name: zmr.name,
                            polygon: this.styleManager.zmrBaseStyle,
                            polyline: this.styleManager.zmrPolylineBaseStyle
                        });

                        zones.polygon.hierarchy = zonesHierarchy;
                        zones.polyline.positions = zmrPositions;

                        ds.entities.add(zones);
                        ds.entities.add(oz);
                    }
                }
            } else {
                console.log('Ошибка загрузки зоны', zone.id);
            }

            // if (ds.entities.values.length !== 2) {
            //     console.log('Ошибка загрузки зоны', zone.id);
            //     console.log(ds.entities.values, ds.entities.values.length);
            // }
            //
            // const [zmr, oz] = ds.entities.values;
            // ds.entities.removeAll();
            //
            // if (!zmr || !oz) {
            //     return;
            // }
            //
            // const zmrPositions = zmr.polygon?.hierarchy.getValue()?.positions;
            // const ozPositions = oz.polygon?.hierarchy.getValue()?.positions;
            //
            // if (!zmrPositions || !ozPositions) {
            //     return;
            // }
            //
            // oz.polygon = this.styleManager.ozBaseStyle;
            // oz.polyline = this.styleManager.ozPolylineBaseStyle;
            // oz.polygon.hierarchy = ozPositions;
            // oz.polyline.positions = ozPositions;
            //
            // const zonesHierarchy = {
            //     positions: zmrPositions,
            //     holes: [{positions: ozPositions}]
            // };
            //
            // const zones = new Cesium.Entity({
            //     id: `zmr_${zone.id}`,
            //     name: zmr.name,
            //     polygon: this.styleManager.zmrBaseStyle,
            //     polyline: this.styleManager.zmrPolylineBaseStyle
            // });
            //
            // zones.polygon.hierarchy = zonesHierarchy;
            // zones.polyline.positions = zmrPositions;
            //
            // ds.entities.add(zones);
            // ds.entities.add(oz);
        })
    }

    async loadProtectionObjects() {
        const protectionObjects = await ApiService.getProtectedObjects();

        const protectionObjectsDataSource = new Cesium.GeoJsonDataSource('protection_objects');
        this.viewer.dataSources.add(protectionObjectsDataSource);

        await protectionObjectsDataSource.load(protectionObjects);

        for (const object of protectionObjectsDataSource.entities.values) {
            if (Cesium.defined(object.polyline)) {
                const objectPosition = object.polyline.positions.getValue();
                object.polyline = this.styleManager.tubeBaseStyle;
                object.polyline.positions = objectPosition;
            } else {
                console.log('Ошибка загрузки охраняемого объекта', object.id);
            }
        }

    }


    // async loadZMR() {
    //     const zones = await ApiService.getZMR();
    //
    //     this.zmr_source.load(zones).then((datasource) => {
    //         datasource.entities.values.forEach((entity) => {
    //             const entityPosition = entity.polygon.hierarchy.getValue().positions
    //             entity.polygon = this.styleManager.zmrBaseStyle
    //             entity.polyline = this.styleManager.zmrPolylineBaseStyle
    //
    //             entity.polygon.hierarchy = entityPosition
    //             entity.polyline.positions = entityPosition
    //         })
    //     })
    // }

    // async loadOZ() {
    //     const zones = await ApiService.getOZ();
    //
    //     this.oz_source.load(zones).then((datasource) => {
    //         datasource.entities.values.forEach((entity) => {
    //             const entityPosition = entity.polygon.hierarchy.getValue().positions
    //             entity.polygon = this.styleManager.ozBaseStyle
    //             entity.polyline = this.styleManager.ozPolylineBaseStyle
    //
    //             entity.polygon.hierarchy = entityPosition
    //             entity.polyline.positions = entityPosition
    //         })
    //     })
    // }

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

            object.polygon = this.styleManager.zmrBaseStyle;
            object.polyline = this.styleManager.zmrPolylineBaseStyle;

            object.polygon.hierarchy = object_geometry
            object.polyline.positions = object_geometry
        }
    }

    highlightObject(object) {
        object.polygon.material = Cesium.Color.BLACK.withAlpha(0.5);
        object.polyline.material = Cesium.Color.BLACK
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

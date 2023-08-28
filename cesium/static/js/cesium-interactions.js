class InteractionManager {
    constructor(viewer) {
        this.viewer = viewer;
    }

    init() {
        this.initLeftClick();
        this.initRightClick();
        this.initDoubleClick();
    }

    initLeftClick() {
        this.viewer.screenSpaceEventHandler.setInputAction((click) => {
            if (click.position !== undefined) {
                let pickedObject = this.viewer.scene.pick(click.position);
                let pickedTiles = this.viewer.imageryLayers.pickImageryLayers(this.viewer.camera.getPickRay(click.position), this.viewer.scene);

                if (Cesium.defined(pickedObject && pickedObject instanceof Cesium.Entity)) {
                    if (pickedObject.id._id.toString().startsWith('zmr')) {
                        // поведение при клике левой кнопкой мыши по зоне минимальных расстояний
                        console.log('Клик левой кнопкой мыши по зоне минимальных расстояний', pickedObject.id.name)
                    } else if (pickedObject.id._id.toString().startsWith('oz')) {
                        // поведение при клике левой кнопкой мыши по охранной зоне
                        console.log('Клик левой кнопкой мыши по охранной зоне', pickedObject.id.name)
                    } else {
                        // поведение при клике левой кнопкой мыши по охраняемому объекту
                        console.log('Клик левой кнопкой мыши по охраняемому объекту', pickedObject.id.name)
                    }
                } else if (Cesium.defined(pickedTiles && pickedTiles instanceof Cesium.ImageryLayer)) {
                    for (const layer of pickedTiles) {
                        if (layer.name.startsWith('Ортофотоплан')) {
                            // поведение при клике левой кнопкой мыши по ортофотоплану
                            console.log('Клик левой кнопкой мыши по ортофотоплану', layer.name.replace('Ортофотоплан ', ''))
                        }
                    }
                }
            }
        }, Cesium.ScreenSpaceEventType.LEFT_CLICK);
    }

    initRightClick() {
        this.viewer.screenSpaceEventHandler.setInputAction((click) => {
            if (click.position !== undefined) {
                let pickedObject = this.viewer.scene.pick(click.position);
                let pickedTiles = this.viewer.imageryLayers.pickImageryLayers(this.viewer.camera.getPickRay(click.position), this.viewer.scene);

                if (Cesium.defined(pickedObject && pickedObject instanceof Cesium.Entity)) {
                    if (pickedObject.id._id.toString().startsWith('zmr')) {
                        // поведение при клике правой кнопкой мыши по зоне минимальных расстояний
                        console.log('Клик правой кнопкой мыши по зоне минимальных расстояний', pickedObject.id.name)
                    } else if (pickedObject.id._id.toString().startsWith('oz')) {
                        // поведение при клике правой кнопкой мыши по охранной зоне
                        console.log('Клик правой кнопкой мыши по охранной зоне', pickedObject.id.name)
                    } else {
                        // поведение при клике правой кнопкой мыши по охраняемому объекту
                        console.log('Клик правой кнопкой мыши по охраняемому объекту', pickedObject.id.name)
                    }
                } else if (Cesium.defined(pickedTiles && pickedTiles instanceof Cesium.ImageryLayer)) {
                    for (const layer of pickedTiles) {
                        if (layer.name.startsWith('Ортофотоплан')) {
                            // поведение при клике правой кнопкой мыши по ортофотоплану
                            console.log('Клик правой кнопкой мыши по ортофотоплану', layer.name.replace('Ортофотоплан ', ''))
                        }
                    }
                }
            }
        }, Cesium.ScreenSpaceEventType.RIGHT_CLICK);
    }

    initDoubleClick() {
        this.viewer.screenSpaceEventHandler.setInputAction((click) => {
            if (click.position !== undefined) {
                let pickedObject = this.viewer.scene.pick(click.position);
                let pickedTiles = this.viewer.imageryLayers.pickImageryLayers(this.viewer.camera.getPickRay(click.position), this.viewer.scene);

                if (Cesium.defined(pickedObject && pickedObject instanceof Cesium.Entity)) {
                    if (pickedObject.id._id.toString().startsWith('zmr')) {
                        // поведение при двойном клике левой кнопкой мыши по зоне минимальных расстояний
                        console.log('Двойной клик левой кнопкой мыши по зоне минимальных расстояний', pickedObject.id.name)
                    } else if (pickedObject.id._id.toString().startsWith('oz')) {
                        // поведение при двойном клике левой кнопкой мыши по охранной зоне
                        console.log('Двойной клик левой кнопкой мыши по охранной зоне', pickedObject.id.name)
                    } else {
                        // поведение при двойном клике левой кнопкой мыши по охраняемому объекту
                        console.log('Двойной клик левой кнопкой мыши по охраняемому объекту', pickedObject.id.name)
                    }
                } else if (Cesium.defined(pickedTiles && pickedTiles instanceof Cesium.ImageryLayer)) {
                    for (const layer of pickedTiles) {
                        if (layer.name.startsWith('Ортофотоплан')) {
                            // поведение при двойном клике левой кнопкой мыши по ортофотоплану
                            console.log('Двойной клик левой кнопкой мыши по ортофотоплану', layer.name.replace('Ортофотоплан ', ''))
                        }
                    }
                }
            }
        }, Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK);
    }
}

// class InteractionManager {
//     constructor(viewer) {
//         this.viewer = viewer;
//     }
//
//     init() {
//         this.initInteraction(Cesium.ScreenSpaceEventType.LEFT_CLICK, "левой", "Клик");
//         this.initInteraction(Cesium.ScreenSpaceEventType.RIGHT_CLICK, "правой", "Клик");
//         this.initInteraction(Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK, "левой", "Двойной клик");
//     }
//
//     initInteraction(eventType, mouseButton, action) {
//         this.viewer.screenSpaceEventHandler.setInputAction((click) => {
//             if (click.position !== undefined) {
//                 const pickedObject = this.viewer.scene.pick(click.position);
//                 const pickedTiles = this.viewer.imageryLayers.pickImageryLayers(this.viewer.camera.getPickRay(click.position), this.viewer.scene);
//
//                 if (Cesium.defined(pickedObject && pickedObject instanceof Cesium.Entity)) {
//                     this.handleEntityClick(pickedObject, mouseButton, action);
//                 } else if (Cesium.defined(pickedTiles && pickedTiles instanceof Cesium.ImageryLayer)) {
//                     this.handleImageryLayerClick(pickedTiles, mouseButton, action);
//                 }
//             }
//         }, eventType);
//     }
//
//     handleEntityClick(pickedObject, mouseButton, action) {
//         const objectId = pickedObject.id;
//         let message = "";
//
//         if (objectId._id.toString().startsWith('zmr')) {
//             message = ` по зоне минимальных расстояний ${objectId.name}`;
//         } else if (objectId._id.toString().startsWith('oz')) {
//             message = ` по охранной зоне ${objectId.name}`;
//         } else {
//             message = ` по охраняемому объекту ${objectId.name}`;
//         }
//
//         console.log(`${action} ${mouseButton} кнопкой мыши${message}`);
//     }
//
//     handleImageryLayerClick(pickedTiles, mouseButton, action) {
//         for (const layer of pickedTiles) {
//             if (layer.name.startsWith('Ортофотоплан')) {
//                 const layerName = layer.name.replace('Ортофотоплан ', '');
//                 console.log(`${action} ${mouseButton} кнопкой мыши по ортофотоплану ${layerName}`);
//             }
//         }
//     }
// }

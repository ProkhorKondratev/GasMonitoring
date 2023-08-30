class LayerPanel {
    constructor(viewer) {
        this.viewer = viewer;
    }

    init() {
        this.layerPanelButton = null
        this.layerPanel = null;

        this.createPanelButton();
        this.createPanel();

        this.dsGroup = new DataSourceGroup(this.viewer);
        this.imgGroup = new ImageryGroup(this.viewer);
        new EntityGroup(this.viewer);

    }

    togglePanel() {
        const isHidden = this.layerPanel.style.display === 'none'

        if (isHidden) {
            this.layerPanel.style.display = 'block'
            this.layerPanel.animate([{opacity: 0}, {opacity: 1}], {duration: 100, fill: 'forwards'})
                .onfinish = () => {
                this.layerPanelButton.title = 'Скрыть панель слоев'
            }
        } else {
            this.layerPanel.animate([{opacity: 1}, {opacity: 0}], {duration: 100, fill: 'forwards'})
                .onfinish = () => {
                this.layerPanel.style.display = 'none'
                this.layerPanelButton.title = 'Показать панель слоев'
            };
        }
    }

    createPanelButton() {
        const cesiumToolbar = document.querySelector(".cesium-viewer-toolbar");
        this.layerPanelButton = document.querySelector(".layers-panel-btn");

        if (!this.layerPanelButton) {
            this.layerPanelButton = document.createElement("button");
            this.layerPanelButton.type = "button";
            this.layerPanelButton.className = "layers-panel-btn";
            this.layerPanelButton.innerHTML = document.getElementById("layers-btn-svg").outerHTML
            this.layerPanelButton.onclick = () => {
                this.togglePanel();
            }
            cesiumToolbar.appendChild(this.layerPanelButton);
        }
    }

    createPanel() {
        const cesiumToolbar = document.querySelector(".cesium-viewer-toolbar");
        this.layerPanel = document.querySelector(".layers-panel");
        if (!this.layerPanel) {
            this.layerPanel = document.createElement("div");
            this.layerPanel.className = "layers-panel";
            this.layerPanel.style.display = "none";
            this.layerPanel.innerHTML = `
                <div class="layers-panel-header">
                    <div class="layers-panel-header-title">Панель слоев</div>
                    <button class="layer-panel-header-btn" title="Обновить список слоев">
                        ${document.getElementById("refresh-btn-svg").outerHTML}
                    </button>
                </div>
                <div class="layers-panel-body"></div>
            `;
            cesiumToolbar.appendChild(this.layerPanel);

            this.layerPanel.querySelector(".layer-panel-header-btn").onclick = () => {
                if (this.dsGroup) this.dsGroup.collectLayers()
                if (this.imgGroup) this.imgGroup.collectLayers()
            }
        }

        document.addEventListener('click', (event) => {
            const path = event.composedPath();
            if (!path.includes(this.layerPanel) &&
                !path.includes(this.layerPanelButton) &&
                this.layerPanel.style.display !== 'none') {
                this.togglePanel();
            }
        });
    }
}

class LayerPanelGroup extends LayerPanel {
    constructor(viewer, layerType, groupName) {
        super(viewer);
        this.layerType = layerType
        this.groupName = groupName

        this.init()
    }

    toggleLayer(layer) {
        const identifier = layer.name || layer.id;
        layer.show = !layer.show;
        document.getElementById('toggle-btn_' + identifier).title = layer.show ? 'Скрыть слой' : 'Показать слой';
        document.getElementById('toggle-btn_' + identifier).innerHTML = layer.show ? document.getElementById(`show-layer-svg`).outerHTML : document.getElementById(`hide-layer-svg`).outerHTML;
    }

    initDraggable() {
        if (!this.draggable) {
            this.draggable = new Draggable.Sortable(document.querySelectorAll(`.${this.layerType}-sector-list`), {
                draggable: '.layers-panel-item',
                handle: '.layers-panel-item',
                distance: 5,
                sortAnimation: {
                    duration: 100,
                    easingFunction: 'ease-in-out',
                },
                mirror: {
                    constrainDimensions: true,
                },
                plugins: [Draggable.Plugins.SortAnimation]
            });
            this.draggable.on('sortable:start', (evt) => {
                evt.data.dragEvent.data.source.style.border = '1px dashed #000';
            })
            this.draggable.on('sortable:sorted', (evt) => {
                this.moveLayer(evt.data.dragEvent.data.source, evt.data.oldIndex, evt.data.newIndex);
            })

            this.draggable.on('sortable:stop', (evt) => {
                this.collectLayers();
            })
        }
    }

    async killDraggable() {
        if (this.draggable) {
            await this.draggable.destroy();
            this.draggable = null;
        }
    }

    createGroup() {
        this.group = document.querySelector(`.layers-panel-${this.layerType}-sector`);
        if (!this.group) {
            this.group = document.createElement('div');
            this.group.className = `layers-panel-${this.layerType}-sector`
            this.group.innerHTML = `
                <div class="${this.layerType}-sector-title">${this.groupName}</div>
                <div class="${this.layerType}-sector-list"></div>
            `;
            document.querySelector('.layers-panel-body').append(this.group)
        }
    }

    async addLayer(layer, layerName = 'Без названия') {
        await this.killDraggable()

        if (!this.group) {
            this.createGroup()
        }
        const identifier = layer.name || layer.id;

        let item = document.getElementById(`${this.layerType}-${identifier}`);
        if (!item && identifier) {
            item = document.createElement('div');
            item.className = 'layers-panel-item';
            item.id = `${this.layerType}-${identifier}`
            item.innerHTML = `
                <div class="layers-panel-item-content">
                    <div class="layers-panel-item-title">${layer.name || layerName}</div>
                    <div class="layers-panel-item-buttons">
                        <button
                            class="layers-panel-item-btn"
                            id="zoom-btn_${identifier}"
                            title="Приблизить к слою">
                            ${document.getElementById(`zoom-to-layer-svg`).outerHTML}
                        </button>
                        <button
                            class="layers-panel-item-btn"
                            id="toggle-btn_${identifier}"
                            title="${layer.show ? 'Скрыть слой' : 'Показать слой'}">
                            ${layer.show ? document.getElementById(`show-layer-svg`).outerHTML : document.getElementById(`hide-layer-svg`).outerHTML}
                        </button>
                    </div>
                </div>
            `;
            document.querySelector(`.${this.layerType}-sector-list`).prepend(item)

            document.getElementById('toggle-btn_' + identifier).onclick = () => {
                this.toggleLayer(layer)
            }
            document.getElementById('zoom-btn_' + identifier).onclick = () => {
                this.viewer.flyTo(layer)
            }
        }
        this.initDraggable();
    }

    removeLayer(layer) {
        const identifier = layer.name || layer.id;
        const item = document.getElementById(`${this.layerType}-${identifier}`);
        if (item) {
            item.remove();
        }
    }
}

class DataSourceGroup extends LayerPanelGroup {
    constructor(viewer, layerType = 'dataSource', groupName = 'Векторные данные') {
        super(viewer, layerType, groupName);
    }

    init() {
        this.appendListeners()
        this.initDraggable();
    }

    appendListeners() {
        this.viewer.dataSources.dataSourceAdded.addEventListener((dataSourceCollection, dataSource) => {
            this.addLayer(dataSource)
        })
        this.viewer.dataSources.dataSourceRemoved.addEventListener((dataSourceCollection, dataSource) => {
            this.removeLayer(dataSource)
        })
    }

    moveLayer(item, initialIndex, newIndex) {
        const layerName = item.id.replace(`${this.layerType}-`, '')
        const dss = this.viewer.dataSources.getByName(layerName);

        if (initialIndex < newIndex) {
            for (let i = initialIndex; i < newIndex; i++) {
                dss.forEach(ds => this.viewer.dataSources.lower(ds));
            }
        } else if (initialIndex > newIndex) {
            for (let i = initialIndex; i > newIndex; i--) {
                dss.forEach(ds => this.viewer.dataSources.raise(ds));
            }
        }
    }

    async collectLayers() {
        await this.killDraggable()

        if (!this.group) {
            this.createGroup()
        }

        document.querySelector(`.${this.layerType}-sector-list`).innerHTML = '';
        for (const ds of this.viewer.dataSources._dataSources) {
            await this.addLayer(ds)
        }
    }
}

class ImageryGroup extends LayerPanelGroup {
    constructor(viewer, layerType = 'imageryLayer', groupName = 'Растровые данные') {
        super(viewer, layerType, groupName);
    }

    init() {
        this.collectLayers()

        this.appendListeners()
        this.initDraggable();
    }

    appendListeners() {
        this.viewer.imageryLayers.layerAdded.addEventListener((imageryLayer) => {
            this.addLayer(imageryLayer)
        })
        this.viewer.imageryLayers.layerRemoved.addEventListener((imageryLayer) => {
            this.removeLayer(imageryLayer)
        })
    }

    moveLayer(item, initialIndex, newIndex) {
        const layerName = item.id.replace(`${this.layerType}-`, '')
        const imageryLayer = this.viewer.imageryLayers._layers.find(l => l.name === layerName);

        if (imageryLayer) {
            if (initialIndex < newIndex) {
                for (let i = initialIndex; i < newIndex; i++) {
                    this.viewer.imageryLayers.lower(imageryLayer);
                }
            } else if (initialIndex > newIndex) {
                for (let i = initialIndex; i > newIndex; i--) {
                    this.viewer.imageryLayers.raise(imageryLayer);
                }
            }
        }

    }

    async collectLayers() {
        await this.killDraggable()

        if (!this.group) {
            this.createGroup()
        }
        document.querySelector(`.${this.layerType}-sector-list`).innerHTML = '';
        for (const imagery of this.viewer.imageryLayers._layers) {
            await this.addLayer(imagery)
        }
    }
}

class EntityGroup extends LayerPanelGroup {
    constructor(viewer, layerType = 'entities', groupName = 'Сущности') {
        super(viewer, layerType, groupName);
    }

    init() {
        this.appendListeners()
    }

    appendListeners() {
        this.viewer.entities.collectionChanged.addEventListener((collection, added, removed, changed) => {
            if (collection.values.length === 0) {
                this.removeLayer(collection)
            } else {
                this.addLayer(collection, 'Объекты')
            }
        })
    }
}
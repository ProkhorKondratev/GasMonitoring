class LayerPanel {
    constructor(viewer) {
        this.viewer = viewer;
    }

    init() {
        this.layerPanelButton = null
        this.layerPanel = null;
        this.swappable = null;

        this.createPanelButton();
        this.createPanel();
        this.appendListeners();

        this.initDraggable();
    }

    togglePanel() {
        if (this.layerPanel.style.display === "none") {
            this.layerPanel.style.display = "block";
        } else {
            this.layerPanel.style.display = "none";
        }
    }

    createPanelButton() {
        const cesiumToolbar = document.querySelector(".cesium-viewer-toolbar");
        this.layerPanelButton = document.createElement("button");
        this.layerPanelButton.type = "button";
        this.layerPanelButton.className = "layers-panel-btn";
        this.layerPanelButton.innerHTML = document.getElementById("layers-btn-svg").outerHTML
        this.layerPanelButton.onclick = () => {
            this.togglePanel();
        }
        cesiumToolbar.appendChild(this.layerPanelButton);
    }

    createPanel() {
        const cesiumToolbar = document.querySelector(".cesium-viewer-toolbar");
        this.layerPanel = document.createElement("div");
        this.layerPanel.className = "layers-panel";
        this.layerPanel.style.display = "none";
        this.layerPanel.innerHTML = `
            <div class="layers-panel-header">
                <div class="layers-panel-header-title">Панель слоев</div>
            </div>
            <div class="layers-panel-body"></div>
        `;

        cesiumToolbar.appendChild(this.layerPanel);
    }

    appendListeners() {
        this.viewer.dataSources.dataSourceAdded.addEventListener((dataSourceCollection, dataSource) => {
            this.addLayer(dataSource)
        });
        this.viewer.dataSources.dataSourceRemoved.addEventListener((dataSourceCollection, dataSource) => {
            this.removeLayer(dataSource)
        });
    }

    initDraggable() {
        if (!this.swappable) {
            this.swappable = new Draggable.Sortable(document.querySelectorAll('.datasource-sector-list'), {
                draggable: '.layers-panel-item',
                handle: '.layers-panel-item-content',
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
            this.swappable.on('sortable:start', (evt) => {
                evt.data.dragEvent.data.source.style.border = '1px dashed #000';
            })
            this.swappable.on('sortable:sorted', (evt) => {
                this.moveDataSource(evt.data.dragEvent.data.source, evt.data.oldIndex, evt.data.newIndex);
            })

            this.swappable.on('sortable:stop', (evt) => {
                this.collectLayers();
            })
        }
    }

    async collectLayers() {
        if (this.swappable) {
            await this.swappable.destroy();
            this.swappable = null;
        }
        console.log('Стирание слоев')
        this.layerPanel.querySelector('.datasource-sector-list').innerHTML = '';

        for (const ds of this.viewer.dataSources._dataSources) {
            const layer = document.createElement('div');
            layer.className = 'layers-panel-item';
            layer.id = 'data-source-' + ds.name;
            layer.innerHTML = `
                <div class="layers-panel-item-content">
                    <div class="layers-panel-item-title">${ds.name}</div>
                    <button 
                        class="layers-panel-item-btn" 
                        id="toggle-btn_${ds.name}" 
                        title="${ds.show ? 'Скрыть слой' : 'Показать слой'}">
                        ${ds.show ? document.getElementById(`show-layer-svg`).outerHTML : document.getElementById(`hide-layer-svg`).outerHTML}
                    </button>
                </div>
            `;
            this.layerPanel.querySelector('.datasource-sector-list').prepend(layer)

            document.getElementById('toggle-btn_' + ds.name).onclick = () => {
                this.toggleDataSource(ds)
            }
        }

        this.initDraggable();
    }

    async addLayer(dataSource) {
        if (this.swappable) {
            await this.swappable.destroy();
            this.swappable = null;
        }

        const dsGroup = this.layerPanel.querySelector('.layers-panel-datasource-sector');
        if (!dsGroup) {
            const dsGroup = document.createElement('div');
            dsGroup.className = 'layers-panel-datasource-sector';
            dsGroup.innerHTML = `
                <div class="datasource-sector-title">Векторные данные</div>
                <div class="datasource-sector-list"></div>
            `;
            this.layerPanel.querySelector('.layers-panel-body').prepend(dsGroup)
        }

        const item = document.getElementById('data-source-' + dataSource.name);
        if (!item) {
            const layer = document.createElement('div');
            layer.className = 'layers-panel-item';
            layer.id = 'data-source-' + dataSource.name;
            layer.innerHTML = `
                <div class="layers-panel-item-content">
                    <div class="layers-panel-item-title">${dataSource.name}</div>
                    <button 
                        class="layers-panel-item-btn" 
                        id="toggle-btn_${dataSource.name}" 
                        title="${dataSource.show ? 'Скрыть слой' : 'Показать слой'}">
                        ${dataSource.show ? document.getElementById(`show-layer-svg`).outerHTML : document.getElementById(`hide-layer-svg`).outerHTML}
                    </button>
                </div>
            `;
            this.layerPanel.querySelector('.datasource-sector-list').prepend(layer)

            document.getElementById('toggle-btn_' + dataSource.name).onclick = () => {
                this.toggleDataSource(dataSource)
            }
        }

        this.initDraggable();
    }

    async removeLayer(dataSource) {
        if (this.swappable) {
            await this.swappable.destroy();
            this.swappable = null;
        }

        const layer = document.getElementById('data-source-' + dataSource.name);
        if (layer) {
            layer.remove()
        }
        this.initDraggable();
    }

    moveDataSource(layer, initialIndex, newIndex) {
        const layerName = layer.id.replace('data-source-', '');
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

    toggleDataSource(dataSource) {
        const showBtn = document.getElementById(`toggle-btn_${dataSource.name}`)
        dataSource.show = !dataSource.show;
        showBtn.innerHTML = dataSource.show ? document.getElementById(`show-layer-svg`).outerHTML : document.getElementById(`hide-layer-svg`).outerHTML
        showBtn.title = dataSource.show ? 'Скрыть слой' : 'Показать слой'
    }
}
class LayerPanel {
    constructor(viewer, containerId) {
        this.viewer = viewer;
        this.container = document.getElementById(containerId);
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

    createPanelButton() {
        const cesiumToolbar = document.querySelector(".cesium-viewer-toolbar");
        this.layerPanelButton = document.createElement("button");
        this.layerPanelButton.type = "button";
        this.layerPanelButton.className = "cesium-layer-panel-btn";
        this.layerPanelButton.innerHTML = document.getElementById("layers-btn-svg").outerHTML
        this.layerPanelButton.onclick = () => {
            this.togglePanel();
        }
        cesiumToolbar.appendChild(this.layerPanelButton);
    }

    createPanel() {
        const cesiumToolbar = document.querySelector(".cesium-viewer-toolbar");
        this.layerPanel = document.createElement("div");
        this.layerPanel.className = "cesium-layers-panel";
        this.layerPanel.style.display = "none";
        this.layerPanel.innerHTML = `
            <div class="cesium-layers-panel-header">
                <div class="cesium-layers-panel-header-title">Панель слоев</div>
            </div>
            <div class="cesium-layers-panel-body"></div>
        `;

        cesiumToolbar.appendChild(this.layerPanel);
    }

    togglePanel() {
        if (this.layerPanel.style.display === "none") {
            this.layerPanel.style.display = "block";
        } else {
            this.layerPanel.style.display = "none";
        }
    }

    initDraggable() {
        this.swappable = new Draggable.Sortable(document.querySelectorAll('.cesium-layers-panel-body-datasource-sector-list'), {
            draggable: '.cesium-layers-panel-body-list-item',
            handle: '.cesium-layers-panel-body-list-item',
        });
        this.swappable.on('sortable:start', (evt) => {
            evt.data.dragEvent.data.source.style.border = '1px dashed #000';
        })
        this.swappable.on('sortable:sorted', (evt) => {
            this.moveLayer(evt.data.dragEvent.data.source, evt.data.oldIndex, evt.data.newIndex);
        })

        this.swappable.on('sortable:stop', (evt) => {
            this.collectLayers();
        })
    }

    async addLayer(dataSource) {
        if (this.swappable) {
            await this.swappable.destroy();
            this.swappable = null;
        }

        const dsGroup = document.querySelector('.cesium-layers-panel-body-datasource-sector')
        if (!dsGroup) {
            const dsGroup = document.createElement('div');
            dsGroup.className = 'cesium-layers-panel-body-datasource-sector';
            dsGroup.innerHTML = `
                <div class="cesium-layers-panel-body-datasource-sector-title">Векторные данные</div>
                <ul class="cesium-layers-panel-body-datasource-sector-list"></ul>
            `;
            this.layerPanel.querySelector('.cesium-layers-panel-body').prepend(dsGroup)
        }

        const item = document.querySelector(`input[name="${dataSource.name}"]`);
        if (!item) {
            const li = document.createElement('li');
            li.className = 'cesium-layers-panel-body-list-item';
            li.innerHTML = `
                <input type="checkbox" id="${dataSource.name}" name="${dataSource.name}" value="${dataSource.name}">
                <label for="${dataSource.name}">${dataSource.name}</label>
            `;
            this.layerPanel.querySelector('.cesium-layers-panel-body-datasource-sector-list').prepend(li)
        }

        this.initDraggable();
    }

    async removeLayer(dataSource) {
        if (this.swappable) {
            await this.swappable.destroy();
            this.swappable = null;
        }

        const layer = document.querySelector(`input[name="${dataSource.name}"]`);
        if (layer) {
            layer.parentNode.remove();
        }
        this.initDraggable();
    }

    async collectLayers() {
        if (this.swappable) {
            await this.swappable.destroy();
            this.swappable = null;
        }
        console.log('Стирание слоев')
        this.layerPanel.querySelector('.cesium-layers-panel-body-datasource-sector-list').innerHTML = '';

        for (const ds of this.viewer.dataSources._dataSources) {
            const li = document.createElement('li');
            li.className = 'cesium-layers-panel-body-list-item';
            li.innerHTML = `
                <input type="checkbox" id="${ds.name}" name="${ds.name}" value="${ds.name}">
                <label for="${ds.name}">${ds.name}</label>
            `;
            this.layerPanel.querySelector('.cesium-layers-panel-body-datasource-sector-list').prepend(li)
        }

        this.initDraggable();
    }

    appendListeners() {
        this.viewer.dataSources.dataSourceAdded.addEventListener((dataSourceCollection, dataSource) => {
            this.addLayer(dataSource)
        });
        this.viewer.dataSources.dataSourceRemoved.addEventListener((dataSourceCollection, dataSource) => {
            this.removeLayer(dataSource)
        });
    }

    moveLayer(layer, initialIndex, newIndex) {

        const layerName = layer.querySelector('label').innerHTML;
        const dss = this.viewer.dataSources.getByName(layerName)

        for (const ds of dss) {
            if (initialIndex < newIndex) {
                for (let i = initialIndex; i < newIndex; i++) {
                    this.viewer.dataSources.lower(ds);
                }
            } else if (initialIndex > newIndex) {
                for (let i = initialIndex; i > newIndex; i--) {
                    this.viewer.dataSources.raise(ds);
                }
            }
        }

    }

}
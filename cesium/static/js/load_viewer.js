function createViewer(api_viewer, containerId, imageryProviderViewModels, terrainProviderViewModels) {
    const base_viewer = new Cesium.Viewer(containerId, {
        baseLayerPicker: api_viewer.baseLayerPicker,
        fullscreenButton: api_viewer.fullscreenButton,
        geocoder: api_viewer.geocoder,
        homeButton: api_viewer.homeButton,
        infoBox: api_viewer.infoBox,
        sceneModePicker: api_viewer.sceneModePicker,
        selectionIndicator: api_viewer.selectionIndicator,
        navigationHelpButton: api_viewer.navigationHelpButton,
        navigationInstructionsInitiallyVisible: api_viewer.navigationInstructionsInitiallyVisible,
        skyAtmosphere: api_viewer.skyAtmosphere === true ? undefined : false,
        fullscreenElement: api_viewer.fullscreenElement,
        targetFrameRate: api_viewer.targetFrameRate,
        showRenderLoopErrors: api_viewer.showRenderLoopErrors,
        sceneMode: api_viewer.sceneMode,
        mapProjection: new Cesium[api_viewer.mapProjection](),
        projectionPicker: api_viewer.projectionPicker,
        globe: api_viewer.globe === true ? undefined : false,
        useBrowserRecommendedResolution: api_viewer.useBrowserRecommendedResolution,

        imageryProviderViewModels: imageryProviderViewModels.imageryProviders,
        terrainProviderViewModels: terrainProviderViewModels.terrainProviders,
    });

    base_viewer._cesiumWidget._creditContainer.style.display = api_viewer.showCredit;
    base_viewer.scene.skyBox.show = api_viewer.skyBox
    base_viewer.scene.sun.show = api_viewer.skyBox
    base_viewer.scene.moon.show = api_viewer.skyBox
    base_viewer.scene.screenSpaceCameraController.minimumZoomDistance = 50

    if (base_viewer.homeButton) {
        base_viewer.homeButton.viewModel.tooltip = 'Вернуться к начальному положению'
    }
    if (base_viewer.fullscreenButton) {
        base_viewer.fullscreenButton.viewModel.tooltip = 'Включить/отключить полноэкранный режим'
    }

    document.querySelector('.cesium-viewer-animationContainer').style.visibility = api_viewer.animation ? 'visible' : 'hidden';
    document.querySelector('.cesium-viewer-timelineContainer').style.visibility = api_viewer.timeline ? 'visible' : 'hidden';

    return base_viewer;
}

async function fetchViewer(containerId, viewerId = null) {
    try {
        const response = await fetch(`/api/cesium_viewers/` + (viewerId ? viewerId : ''));
        const data = await response.json()
        const api_viewer = viewerId ? data : data.find(viewer => viewer.is_default);

        if (api_viewer) {
            const imageryProviderViewModels = await fetchTileProviders(api_viewer.imageryProviderViewModels);
            const terrainProviderViewModels = await fetchTileProviders(api_viewer.terrainProviderViewModels);
            return createViewer(api_viewer, containerId, imageryProviderViewModels, terrainProviderViewModels);
        } else {
            console.error('Отсутствует базовый Viewer');
            return new Cesium.Viewer(containerId);
        }
    } catch (error) {
        console.error(error);
    }
}
from django.contrib import admin
from cesium.models import TileProvider, ProviderViewModel, CesiumViewer


@admin.register(TileProvider)
class TileProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'url')
    list_display_links = ('name',)


@admin.register(ProviderViewModel)
class ProviderViewModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'is_enabled', 'tileProvider')
    list_display_links = ('name',)


@admin.register(CesiumViewer)
class CesiumViewerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_default')
    list_display_links = ('id', 'name')

    fieldsets = (
        ('', {'fields': (('name', 'is_default'),)}),
        ('Панель управления',
         {'fields': (
             'baseLayerPicker', 'fullscreenButton', 'geocoder', 'homeButton', 'sceneModePicker', 'navigationHelpButton',
             'navigationInstructionsInitiallyVisible', 'projectionPicker', ('timeline', 'animation'))}),
        ('Поведение', {'fields': ('sceneMode', 'showRenderLoopErrors', 'selectionIndicator', 'infoBox')}),
        ('Параметры',
         {'fields': ('imageryProviderViewModels', 'terrainProviderViewModels', ('skyBox', 'skyAtmosphere', 'globe'),
                     'targetFrameRate', 'mapProjection', 'showCredit', 'fullscreenElement')}),

    )

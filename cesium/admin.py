from django.contrib import admin
from cesium import models as cesium_models
from django.db import models
from django_json_widget.widgets import JSONEditorWidget


@admin.register(cesium_models.TileProvider)
class TileProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'url')
    list_display_links = ('name',)


@admin.register(cesium_models.ProviderViewModel)
class ProviderViewModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'is_enabled', 'tileProvider')
    list_display_links = ('name',)


@admin.register(cesium_models.CesiumViewer)
class CesiumViewerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_default')
    list_display_links = ('id', 'name')

    fieldsets = (
        ('',
         {'fields': ('name', 'is_default')}),
        ('Панель управления',
         {'fields': (
             'baseLayerPicker', 'fullscreenButton', 'geocoder', 'homeButton', 'sceneModePicker', 'navigationHelpButton',
             'navigationInstructionsInitiallyVisible', 'projectionPicker', ('timeline', 'animation'))}),
        ('Поведение',
         {'fields': (
             'sceneMode', 'showRenderLoopErrors', 'selectionIndicator', 'infoBox', 'useBrowserRecommendedResolution')}),
        ('Параметры',
         {'fields': ('imageryProviderViewModels', 'terrainProviderViewModels', ('skyBox', 'skyAtmosphere', 'globe'),
                     'targetFrameRate', 'mapProjection', 'showCredit', 'fullscreenElement')}),

    )


@admin.register(cesium_models.CesiumBillboard)
class CesiumBillboardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image', 'is_default')
    list_display_links = ('id', 'name')
    fieldsets = (
        ('',
         {'fields': ('name', 'show', 'is_default', 'image')}),
        ('Стиль',
         {'fields': ('color',)}),
        ('Размеры',
         {'fields': ('scale', 'width', 'height')}),
        ('Положение',
         {'fields': ('heightReference', 'rotation', 'alignedAxis', ('horizontalOrigin', 'verticalOrigin'))}),
        ('Параметры отображения',
         {'fields': (('pixelOffset', 'eyeOffset'), 'scaleByDistance', 'translucencyByDistance',
                     'pixelOffsetScaleByDistance', 'distanceDisplayCondition')}),
    )

    formfield_overrides = {models.JSONField: {'widget': JSONEditorWidget(width='100%', height='auto')}}


@admin.register(cesium_models.CesiumLabel)
class CesiumLabelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text', 'is_default')
    list_display_links = ('id', 'name')
    fieldsets = (
        ('',
         {'fields': ('name', 'show', 'is_default', 'text')}),
        ('Параметры стиля',
         {'fields': ('font', 'style', 'scale', 'showBackground')}),
        ('Стиль',
         {'fields': (('fillColor', 'outlineColor'), 'backgroundColor', 'backgroundPadding', 'outlineWidth')}),
        ('Положение',
         {'fields': ('heightReference', ('horizontalOrigin', 'verticalOrigin'))}),
        ('Параметры отображения',
         {'fields': (
             ('pixelOffset', 'eyeOffset'), ('translucencyByDistance', 'pixelOffsetScaleByDistance'),
             ('scaleByDistance', 'distanceDisplayCondition'))}),
    )

    formfield_overrides = {models.JSONField: {'widget': JSONEditorWidget(width='100%', height='auto')}}


@admin.register(cesium_models.CesiumPoint)
class CesiumPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_default')
    list_display_links = ('id', 'name')
    fieldsets = (
        ('',
         {'fields': ('name', 'show', 'is_default')}),
        ('Размеры',
         {'fields': (('pixelSize', 'outlineWidth'),)}),
        ('Стиль',
         {'fields': (('color', 'outlineColor'),)}),
        ('Положение',
         {'fields': ('heightReference',)}),
        ('Параметры отображения',
         {'fields': ('translucencyByDistance', 'distanceDisplayCondition', 'scaleByDistance')}),
    )

    formfield_overrides = {models.JSONField: {'widget': JSONEditorWidget(width='100%', height='auto')}}


@admin.register(cesium_models.CesiumPolyline)
class CesiumPolylineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_default')
    list_display_links = ('id', 'name')
    fieldsets = (
        ('',
         {'fields': ('name', 'show', 'is_default')}),
        ('Размеры', {'fields': ('width',)}),
        ('Стиль',
         {'fields': (('material', 'depthFailMaterial'),)}),
        ('Положение',
         {'fields': ('clampToGround',)}),
        ('Параметры отображения',
         {'fields': ('shadows', 'distanceDisplayCondition', 'zIndex')}),
    )

    formfield_overrides = {models.JSONField: {'widget': JSONEditorWidget(width='100%', height='auto')}}


@admin.register(cesium_models.CesiumPolygon)
class CesiumPolygonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_default')
    list_display_links = ('id', 'name')
    fieldsets = (
        ('',
         {'fields': ('name', 'show', 'is_default')}),
        ('Параметры стиля',
         {'fields': ('fill', 'outline', 'closeTop', 'closeBottom')}),
        ('Стиль',
         {'fields': ('material', ('outlineColor', 'outlineWidth'))}),
        ('Положение',
         {'fields': ('heightReference', 'height', 'extrudedHeightReference', 'extrudedHeight', 'stRotation')}),
        ('Параметры отображения',
         {'fields': ('shadows', 'distanceDisplayCondition', 'zIndex')}),
    )

    formfield_overrides = {models.JSONField: {'widget': JSONEditorWidget(width='100%', height='auto')}}


@admin.register(cesium_models.CesiumPolylineMaterial)
class CesiumPolylineMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_default')
    list_display_links = list_display

    fieldsets = (
        ('', {
            'fields': ('name', 'type', 'is_default'),
        }),
        ('Стандартные настройки', {
            'fields': ('color',),
        }),
        ('Пунктирная линия', {
            'fields': ('gapColor', 'dashLength'),
        }),
    )


@admin.register(cesium_models.CesiumPolygonMaterial)
class CesiumPolygonMaterialStyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_default')
    list_display_links = list_display

    fieldsets = (
        ('', {
            'fields': ('name', 'type', 'color', 'is_default'),
        }),
    )

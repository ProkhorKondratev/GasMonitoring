from django.urls import path
from .views import MapView
from . import serializers as api

view_sets = [
    (r'provider_models', api.ProviderViewModelViewSet, 'provider_models'),
    (r'cesium_viewers', api.CesiumViewerViewSet, 'cesium_viewers'),

    (r'billboard_styles', api.CesiumBillboardViewSet, 'billboard_styles'),
    (r'label_styles', api.CesiumLabelViewSet, 'label_styles'),
    (r'point_styles', api.CesiumPointViewSet, 'point_styles'),
    (r'polyline_styles', api.CesiumPolylineViewSet, 'polyline_styles'),
    (r'polygon_styles', api.CesiumPolygonViewSet, 'polygon_styles'),

    (r'polyline_material_styles', api.CesiumPolylineMaterialViewSet, 'polyline_material_styles'),
    (r'polygon_material_styles', api.CesiumPolygonMaterialViewSet, 'polygon_material_styles'),
]

urlpatterns = [
    path("map", MapView.as_view(), name="map"),
]

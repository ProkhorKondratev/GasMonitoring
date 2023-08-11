from django.urls import path
from .views import MapView
from . import serializers as api

view_sets = [
    (r'provider_models', api.ProviderViewModelViewSet, 'provider_models'),
    (r'cesium_viewers', api.CesiumViewerViewSet, 'cesium_viewers'),

    (r'cesium_billboards', api.CesiumBillboardViewSet, 'cesium_billboards'),
    (r'cesium_labels', api.CesiumLabelViewSet, 'cesium_labels'),
    (r'cesium_points', api.CesiumPointViewSet, 'cesium_points'),
    (r'cesium_polylines', api.CesiumPolylineViewSet, 'cesium_polylines'),
    (r'cesium_polygons', api.CesiumPolygonViewSet, 'cesium_polygons'),

    (r'cesium_polyline_materials', api.CesiumPolylineMaterialViewSet, 'cesium_polyline_materials'),
    (r'cesium_polygon_materials', api.CesiumPolygonMaterialViewSet, 'cesium_polygon_materials'),
]

urlpatterns = [
    path("map", MapView.as_view(), name="map"),
]

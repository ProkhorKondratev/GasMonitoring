from django.urls import path
from .views import MapView
from . import serializers as api

view_sets = [
    (r'provider_views', api.ProviderViewModelViewSet, 'provider_views'),
    (r'cesium_viewers', api.CesiumViewerViewSet, 'cesium_viewers'),
]

urlpatterns = [
    path("map", MapView.as_view(), name="map"),
]

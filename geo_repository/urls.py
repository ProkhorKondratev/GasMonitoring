from geo_repository import serializers as api
from geo_repository.views import tiles
from django.urls import path

view_sets = [
    (r'zmr', api.ZMRViewSet, 'zmr'),
    (r'zmr_geom', api.ZMRGeometryViewSet, 'zmr_geom'),
    (r'oz', api.OZViewSet, 'oz'),
    (r'oz_geom', api.OZGeometryViewSet, 'oz_geom'),
    (r'protection_zones_geom', api.ProtectionZonesViewSet, 'protection_zones_geom'),
    (r'protected_object_geom', api.ProtectedObjectGeometryViewSet, 'protected_object_geom'),
    ('geodata_files', api.GeoDataFileViewSet, 'geodata_files'),
]

urlpatterns = [
    path("tiles/<str:tiles_type>/<int:database_id>/<int:z>/<int:x>/<int:y>", tiles, name="tiles")
]

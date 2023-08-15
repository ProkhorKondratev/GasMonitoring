from . import serializers as api

view_sets = [
    (r'zmr', api.ZMRViewSet, 'zmr'),
    (r'zmr_geom', api.ZMRGeometryViewSet, 'zmr_geom'),
    (r'oz', api.OZViewSet, 'oz'),
    (r'oz_geom', api.OZGeometryViewSet, 'oz_geom'),
]

urlpatterns = []

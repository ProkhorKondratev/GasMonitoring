from . import serializers as api

view_sets = [
    (r'zmrs', api.ZMRViewSet, 'zmrs'),
    (r'zmr_geometries', api.ZMRGeometryViewSet, 'zmr_geometries'),
]

urlpatterns = []

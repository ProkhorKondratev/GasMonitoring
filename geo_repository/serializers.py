from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import ZMR, ZMRGeometry
from rest_framework.viewsets import ModelViewSet


class ZMRSerializer(serializers.ModelSerializer):
    zmr_geometry = serializers.SerializerMethodField()

    @staticmethod
    def get_zmr_geometry(obj):
        return ZMRGeometrySerializer(obj.zmr_geometry.get(is_relevant=True)).data

    class Meta:
        model = ZMR
        fields = '__all__'


class ZMRViewSet(ModelViewSet):
    queryset = ZMR.objects.all()
    serializer_class = ZMRSerializer


class ZMRGeometrySerializer(GeoFeatureModelSerializer):
    date_start = serializers.DateTimeField(format='%d.%m.%Y - %H:%M', read_only=True)
    date_end = serializers.DateTimeField(format='%d.%m.%Y - %H:%M', read_only=True)
    is_relevant = serializers.BooleanField(read_only=True)
    zone = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(source='zone.name', read_only=True)

    class Meta:
        model = ZMRGeometry
        geo_field = "geom"
        fields = '__all__'


class ZMRGeometryViewSet(ModelViewSet):
    queryset = ZMRGeometry.objects.all()
    serializer_class = ZMRGeometrySerializer

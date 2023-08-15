from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import ZMR, ZMRGeometry, OZ, OZGeometry
from rest_framework.viewsets import ModelViewSet


class ZMRSerializer(serializers.ModelSerializer):
    zmr_geometry = serializers.SerializerMethodField()

    @staticmethod
    def get_zmr_geometry(obj):
        try:
            geom = obj.zmr_geometry.get(is_relevant=True)
        except OZGeometry.DoesNotExist:
            return None
        return OZGeometrySerializer(geom).data

    class Meta:
        model = ZMR
        fields = '__all__'


class ZMRViewSet(ModelViewSet):
    queryset = ZMR.objects.all()
    serializer_class = ZMRSerializer

    def get_queryset(self):
        queryset = ZMR.objects.all()
        is_show = self.request.query_params.get('is_show', None)
        if is_show is not None:
            queryset = queryset.filter(is_show=is_show)
        return queryset


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

    def get_queryset(self):
        # показываем только тот у которого в ZMR.is_show = True
        queryset = ZMRGeometry.objects.filter(is_relevant=True)
        zone_id = self.request.query_params.get('zone_id', None)
        if zone_id is not None:
            queryset = queryset.filter(zone_id=zone_id)
        else:
            queryset = queryset.filter(zone__is_show=True)
        return queryset


class OZSerializer(serializers.ModelSerializer):
    oz_geometry = serializers.SerializerMethodField()

    @staticmethod
    def get_oz_geometry(obj):
        try:
            geom = obj.oz_geometry.get(is_relevant=True)
        except OZGeometry.DoesNotExist:
            return None
        return OZGeometrySerializer(geom).data

    class Meta:
        model = OZ
        fields = '__all__'


class OZViewSet(ModelViewSet):
    queryset = OZ.objects.all()
    serializer_class = OZSerializer

    def get_queryset(self):
        queryset = OZ.objects.all()
        is_show = self.request.query_params.get('is_show', None)
        if is_show is not None:
            queryset = queryset.filter(is_show=is_show)
        return queryset


class OZGeometrySerializer(GeoFeatureModelSerializer):
    date_start = serializers.DateTimeField(format='%d.%m.%Y - %H:%M', read_only=True)
    date_end = serializers.DateTimeField(format='%d.%m.%Y - %H:%M', read_only=True)
    is_relevant = serializers.BooleanField(read_only=True)
    zone = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = OZGeometry
        geo_field = "geom"
        fields = '__all__'


class OZGeometryViewSet(ModelViewSet):
    queryset = OZGeometry.objects.all()
    serializer_class = OZGeometrySerializer

    def get_queryset(self):
        # показываем только тот у которого в OZ.is_show = True
        queryset = OZGeometry.objects.filter(is_relevant=True)
        zone_id = self.request.query_params.get('zone_id', None)
        if zone_id is not None:
            queryset = queryset.filter(zone_id=zone_id)
        else:
            queryset = queryset.filter(zone__is_show=True)
        return queryset

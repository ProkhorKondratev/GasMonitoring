from django.contrib.gis.geos import GeometryCollection
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from rest_framework import serializers
from .models import ZMR, ZMRGeometry, OZ, OZGeometry, ProtectedObject, ProtectedObjectGeometry
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
    parent_object = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(source='parent_object.name', read_only=True)

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
        parent_id = self.request.query_params.get('id', None)
        if parent_id is not None:
            queryset = queryset.filter(parent_object_id=parent_id)
        else:
            queryset = queryset.filter(parent_object__is_show=True)
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
    parent_object = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(source='parent_object.name', read_only=True)

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
        parent_id = self.request.query_params.get('id', None)
        if parent_id is not None:
            queryset = queryset.filter(parent_object_id=parent_id)
        else:
            queryset = queryset.filter(parent_object__is_show=True)
        return queryset


class ProtectedObjectSerializer(GeoFeatureModelSerializer):
    geom = GeometrySerializerMethodField()

    @staticmethod
    def get_geom(obj):
        related_zmr = obj.protection_zmr.first()
        zone_geom = related_zmr.zmr_geometry.get(is_relevant=True) if related_zmr else None

        related_oz = obj.protection_oz.first()
        oz_geom = related_oz.oz_geometry.get(is_relevant=True) if related_oz else None

        protected_object_geom = obj.protected_object_geometry.get(is_relevant=True)

        if zone_geom and oz_geom and protected_object_geom:
            return GeometryCollection([zone_geom.geom, oz_geom.geom]).union(protected_object_geom.geom)

    class Meta:
        model = ProtectedObject
        geo_field = "geom"
        fields = '__all__'


class ProtectedObjectViewSet(ModelViewSet):
    queryset = ProtectedObject.objects.all()
    serializer_class = ProtectedObjectSerializer

    def get_queryset(self):
        queryset = ProtectedObject.objects.all()
        is_show = self.request.query_params.get('is_show', None)
        if is_show is not None:
            queryset = queryset.filter(is_show=is_show)
        return queryset


class ProtectedObjectGeometrySerializer(GeoFeatureModelSerializer):
    date_start = serializers.DateTimeField(format='%d.%m.%Y - %H:%M', read_only=True)
    date_end = serializers.DateTimeField(format='%d.%m.%Y - %H:%M', read_only=True)
    is_relevant = serializers.BooleanField(read_only=True)
    parent_object = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(source='parent_object.name', read_only=True)

    class Meta:
        model = ProtectedObjectGeometry
        geo_field = "geom"
        fields = '__all__'


class ProtectedObjectGeometryViewSet(ModelViewSet):
    queryset = ProtectedObjectGeometry.objects.all()
    serializer_class = ProtectedObjectGeometrySerializer

    def get_queryset(self):
        # показываем только тот у которого в ProtectedObject.is_show = True
        queryset = ProtectedObjectGeometry.objects.filter(is_relevant=True)
        parent_id = self.request.query_params.get('id', None)
        if parent_id is not None:
            queryset = queryset.filter(parent_object_id=parent_id)
        else:
            queryset = queryset.filter(parent_object__is_show=True)
        return queryset

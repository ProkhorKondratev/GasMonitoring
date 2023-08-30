from django.contrib.gis.geos import GeometryCollection
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometrySerializerMethodField
from rest_framework.response import Response
from rest_framework import serializers
from .models import ZMR, ZMRGeometry, OZ, OZGeometry, ProtectedObject, ProtectedObjectGeometry
from .geodata_models import GeoDataFile
from rest_framework.viewsets import ModelViewSet
import sqlite3
from django.contrib.gis.geos import Point, MultiPoint


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
            queryset = queryset.filter(is_show=True)
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
            queryset = queryset.filter(is_show=True)
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
        queryset = OZGeometry.objects.filter(is_relevant=True)
        parent_id = self.request.query_params.get('id', None)
        if parent_id is not None:
            queryset = queryset.filter(parent_object_id=parent_id)
        else:
            queryset = queryset.filter(parent_object__is_show=True)
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


class ProtectionZonesSerializer(serializers.ModelSerializer):
    zmr_geom = GeometrySerializerMethodField()
    oz_geom = GeometrySerializerMethodField()

    @staticmethod
    def get_zmr_geom(obj):
        related_zmr = obj.protection_zmr.first()
        zone_geom = related_zmr.zmr_geometry.get(is_relevant=True) if related_zmr else None
        return zone_geom.geom if zone_geom else None

    @staticmethod
    def get_oz_geom(obj):
        related_oz = obj.protection_oz.first()
        oz_geom = related_oz.oz_geometry.get(is_relevant=True) if related_oz else None
        return oz_geom.geom if oz_geom else None

    # geom = GeometrySerializerMethodField()
    #
    # @staticmethod
    # def get_geom(obj):
    #     related_zmr = obj.protection_zmr.first()
    #     zone_geom = related_zmr.zmr_geometry.get(is_relevant=True) if related_zmr else None
    #
    #     related_oz = obj.protection_oz.first()
    #     oz_geom = related_oz.oz_geometry.get(is_relevant=True) if related_oz else None
    #
    #     if zone_geom and oz_geom:
    #         return GeometryCollection([zone_geom.geom, oz_geom.geom])

    class Meta:
        model = ProtectedObject
        fields = '__all__'


class ProtectionZonesViewSet(ModelViewSet):
    queryset = ProtectedObject.objects.all()
    serializer_class = ProtectionZonesSerializer

    def get_queryset(self):
        queryset = ProtectedObject.objects.all()
        is_show = self.request.query_params.get('is_show', None)
        if is_show is not None:
            queryset = queryset.filter(is_show=True)
        return queryset


class GeoDataFileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    # rectangle = GeometrySerializerMethodField()
    #
    # @staticmethod
    # def get_rectangle(obj):
    #     conn = sqlite3.connect(obj.path)
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT min_x, min_y, max_x, max_y FROM gpkg_contents")
    #     result = cursor.fetchone()
    #     conn.close()
    #     return MultiPoint([
    #         Point(result[0], result[1], srid=3857),
    #         Point(result[2], result[3], srid=3857)], srid=3857) \
    #         .envelope.transform(4326, clone=True)

    @staticmethod
    def get_url(obj):
        return f'/tiles/relt/{obj.id}/{{z}}/{{x}}/{{y}}'

    class Meta:
        model = GeoDataFile
        fields = '__all__'


class GeoDataFileViewSet(ModelViewSet):
    queryset = GeoDataFile.objects.all()
    serializer_class = GeoDataFileSerializer

    def create(self, request, *args, **kwargs):
        try:
            obj = GeoDataFile.objects.get(path=request.data['path'])
            obj.path = request.data['path']
            obj.save()
            return Response(status=200, data={'message': 'Обновлено'})

        except GeoDataFile.DoesNotExist:
            super().create(request, *args, **kwargs)
            return Response(status=201, data={'message': 'Создано'})

    def get_queryset(self):
        queryset = GeoDataFile.objects.all()
        is_show = self.request.query_params.get('is_show', None)
        if is_show is not None:
            queryset = queryset.filter(is_show=True)
        return queryset

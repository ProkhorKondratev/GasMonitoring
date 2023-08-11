from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from cesium import models as cesium_models
from rest_framework.permissions import AllowAny


class ProviderViewModelSerializer(ModelSerializer):
    class Meta:
        model = cesium_models.ProviderViewModel
        fields = '__all__'
        depth = 2


class ProviderViewModelViewSet(ModelViewSet):
    queryset = cesium_models.ProviderViewModel.objects.all()
    serializer_class = ProviderViewModelSerializer
    permission_classes = (AllowAny,)


class CesiumViewerSerializer(ModelSerializer):
    class Meta:
        model = cesium_models.CesiumViewer
        fields = '__all__'
        depth = 3


class CesiumViewerViewSet(ModelViewSet):
    queryset = cesium_models.CesiumViewer.objects.all()
    serializer_class = CesiumViewerSerializer
    permission_classes = (AllowAny,)


class CesiumBillboardSerializer(ModelSerializer):
    class Meta:
        model = cesium_models.CesiumBillboard
        fields = '__all__'


class CesiumBillboardViewSet(ModelViewSet):
    queryset = cesium_models.CesiumBillboard.objects.all()
    serializer_class = CesiumBillboardSerializer
    permission_classes = (AllowAny,)


class CesiumLabelSerializer(ModelSerializer):
    class Meta:
        model = cesium_models.CesiumLabel
        fields = '__all__'


class CesiumLabelViewSet(ModelViewSet):
    queryset = cesium_models.CesiumLabel.objects.all()
    serializer_class = CesiumLabelSerializer
    permission_classes = (AllowAny,)


class CesiumPointSerializer(ModelSerializer):
    class Meta:
        model = cesium_models.CesiumPoint
        fields = '__all__'


class CesiumPointViewSet(ModelViewSet):
    queryset = cesium_models.CesiumPoint.objects.all()
    serializer_class = CesiumPointSerializer
    permission_classes = (AllowAny,)


class CesiumPolylineSerializer(ModelSerializer):
    class Meta:
        model = cesium_models.CesiumPolyline
        exclude = ('heightReference', 'scaleByDistance', 'translucencyByDistance')


class CesiumPolylineViewSet(ModelViewSet):
    queryset = cesium_models.CesiumPolyline.objects.all()
    serializer_class = CesiumPolylineSerializer
    permission_classes = (AllowAny,)


class CesiumPolygonSerializer(ModelSerializer):
    class Meta:
        model = cesium_models.CesiumPolygon
        exclude = ('scaleByDistance', 'translucencyByDistance')


class CesiumPolygonViewSet(ModelViewSet):
    queryset = cesium_models.CesiumPolygon.objects.all()
    serializer_class = CesiumPolygonSerializer
    permission_classes = (AllowAny,)


class CesiumPolylineMaterialSerializer(ModelSerializer):
    class Meta:
        model = cesium_models.CesiumPolylineMaterial
        fields = '__all__'


class CesiumPolylineMaterialViewSet(ModelViewSet):
    queryset = cesium_models.CesiumPolylineMaterial.objects.all()
    serializer_class = CesiumPolylineMaterialSerializer
    permission_classes = (AllowAny,)


class CesiumPolygonMaterialSerializer(ModelSerializer):
    class Meta:
        model = cesium_models.CesiumPolygonMaterial
        fields = '__all__'


class CesiumPolygonMaterialViewSet(ModelViewSet):
    queryset = cesium_models.CesiumPolygonMaterial.objects.all()
    serializer_class = CesiumPolygonMaterialSerializer
    permission_classes = (AllowAny,)

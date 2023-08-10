from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet
from .models import ProviderViewModel, CesiumViewer
from rest_framework.permissions import AllowAny


class ProviderViewModelSerializer(ModelSerializer):
    class Meta:
        model = ProviderViewModel
        fields = '__all__'
        depth = 2


class ProviderViewModelViewSet(ModelViewSet):
    queryset = ProviderViewModel.objects.all()
    serializer_class = ProviderViewModelSerializer
    permission_classes = (AllowAny,)


class CesiumViewerSerializer(ModelSerializer):
    class Meta:
        model = CesiumViewer
        fields = '__all__'
        depth = 3


class CesiumViewerViewSet(ModelViewSet):
    queryset = CesiumViewer.objects.all()
    serializer_class = CesiumViewerSerializer
    permission_classes = (AllowAny,)

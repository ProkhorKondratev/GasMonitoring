from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers

from cesium.urls import view_sets as cesium_view_sets, urlpatterns as cesium_urls
from geo_repository.urls import view_sets as geo_view_sets, urlpatterns as geo_urls

router = routers.DefaultRouter()
router.registry.extend(cesium_view_sets)
router.registry.extend(geo_view_sets)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('', include(cesium_urls)),
    path('', include(geo_urls)),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

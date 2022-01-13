"""THE_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from tindall_haul_erect.views import DriverViewSet, BasicDriverViewSet, LoadViewSet


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

driver_router = routers.DefaultRouter()
driver_router.register(r'drivers', DriverViewSet, basename='drivers')

basic_driver_router = routers.DefaultRouter()
basic_driver_router.register(r'basic_drivers', BasicDriverViewSet, basename='basic_drivers')

load_router = routers.DefaultRouter()
load_router.register(r'loads', LoadViewSet, basename='loads')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(driver_router.urls)),
    path('', include(basic_driver_router.urls)),
    path('', include(load_router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

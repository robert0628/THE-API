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
from rest_framework import routers
from tindall_haul_erect.views import DriverViewSet, BasicDriverViewSet, LoadViewSet, PreStressBillingLookupViewSet, \
    UtilitiesBillingLookupViewSet

# Routers provide an easy way of automatically determining the URL conf. for ModelViewsets

driver_router = routers.DefaultRouter()
driver_router.register(r'drivers', DriverViewSet, basename='drivers')

basic_driver_router = routers.DefaultRouter()
basic_driver_router.register(r'basic_drivers', BasicDriverViewSet, basename='basic_drivers')

load_router = routers.DefaultRouter()
load_router.register(r'loads', LoadViewSet, basename='loads')

prestress_billing_lookup_router = routers.DefaultRouter()
prestress_billing_lookup_router.register(r'prestress_billing_lookup', PreStressBillingLookupViewSet,
                                         basename='prestress_billing_lookup')

utilities_billing_lookup_router = routers.DefaultRouter()
utilities_billing_lookup_router.register(r'utilities_billing_lookup', UtilitiesBillingLookupViewSet,
                                         basename='utilities_billing_lookup')

urlpatterns = [
    path('', include(driver_router.urls)),
    path('', include(basic_driver_router.urls)),
    path('', include(load_router.urls)),
    path('', include(prestress_billing_lookup_router.urls)),
    path('', include(utilities_billing_lookup_router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

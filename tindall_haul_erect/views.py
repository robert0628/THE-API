from .models import Driver, Load, PreStressBillingLookup, UtilitiesBillingLookup, Billing, RateLookup, \
    UnloadingTimeLookup, DriverSettlement, SiteSettlement
from .serializers import DriverSerializer, BasicDriverSerializer, LoadSerializer, PreStressBillingLookupSerializer, \
    UtilitiesBillingLookupSerializer, BillingSerializer, RateLookupSerializer, UnloadingTimeLookupSerializer, \
    DriverSettlementSerializer, SiteSettlementSerializer
from rest_framework import viewsets
from rest_framework import filters
from django_filters import rest_framework as df_filters
from .filters import DriverFilter


# Create your views here.


class DriverViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing all driver information
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filterset_class = DriverFilter


class BasicDriverViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing basic driver information
    """
    queryset = Driver.objects.all()
    serializer_class = BasicDriverSerializer


class LoadViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing load information
    """
    queryset = Load.objects.all()
    serializer_class = LoadSerializer


class PreStressBillingLookupViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing pre-stress billing lookup information
    """
    queryset = PreStressBillingLookup.objects.all()
    serializer_class = PreStressBillingLookupSerializer


class UtilitiesBillingLookupViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing utilities billing lookup information
    """
    queryset = UtilitiesBillingLookup.objects.all()
    serializer_class = UtilitiesBillingLookupSerializer


class BillingViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing all billing information
    """
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer


class RateLookupViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing the rate lookup information
    """
    queryset = RateLookup.objects.all()
    serializer_class = RateLookupSerializer


class UnloadingTimeLookupViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing the rate lookup information
    """
    queryset = UnloadingTimeLookup.objects.all()
    serializer_class = UnloadingTimeLookupSerializer


class DriverSettlementViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing the driver settlements
    """
    queryset = DriverSettlement.objects.all()
    serializer_class = DriverSettlementSerializer


class SiteSettlementViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing the site settlements
    """
    queryset = SiteSettlement.objects.all()
    serializer_class = SiteSettlementSerializer

from .models import Driver, Load, PreStressBillingLookup, UtilitiesBillingLookup, Billing, RateLookup, \
    UnloadingTimeLookup
from .serializers import DriverSerializer, BasicDriverSerializer, LoadSerializer, PreStressBillingLookupSerializer, \
    UtilitiesBillingLookupSerializer, BillingSerializer, RateLookupSerializer, UnloadingTimeLookupSerializer
from rest_framework import viewsets


# Create your views here.


class DriverViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing all driver information
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


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

from .models import Driver, Load, PreStressBillingLookup, UtilitiesBillingLookup, Billing, RateLookup, \
    UnloadingTimeLookup, DriverSettlement, SiteSettlement
from .serializers import DriverSerializer, BasicDriverSerializer, LoadSerializer, PreStressBillingLookupSerializer, \
    UtilitiesBillingLookupSerializer, BillingSerializer, RateLookupSerializer, UnloadingTimeLookupSerializer, \
    DriverSettlementSerializer, SiteSettlementSerializer
from rest_framework import viewsets
from .filters import DriverFilter, LoadFilter
from rest_framework.pagination import PageNumberPagination


class PageNumberWithPageSizePagination(PageNumberPagination):
    """
    Description:
    This class can be used so the api endpoint can accept paginating parameters in the request.
    by Default PageNumberPagination has page_size_query_param set to None, this needs to be override
    to be able to ser Rows per page.
    set the pagination_class attribute in a viewset to this class.

    Example:
        class View(viewsets.ModelViewSet):
            ...
            pagination_class = PageNumberWithPageSizePagination
    """
    page_size_query_param = 'page_size'


# The default filter backend was set globally which allows the use of filterset_class see the settings.py

class DriverViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing all driver information
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    filterset_class = DriverFilter
    pagination_class = PageNumberWithPageSizePagination


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
    filterset_class = LoadFilter
    pagination_class = PageNumberWithPageSizePagination


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

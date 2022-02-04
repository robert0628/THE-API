from .models import Driver, Load, PreStressBillingLookup, UtilitiesBillingLookup, Billing, Rate, \
    UnloadingTimeLookup, DriverSettlement, SiteSettlement
from .serializers import DriverSerializer, BasicDriverSerializer, LoadSerializer, PreStressBillingLookupSerializer, \
    UtilitiesBillingLookupSerializer, BillingSerializer, RateSerializer, UnloadingTimeLookupSerializer, \
    DriverSettlementSerializer, SiteSettlementSerializer
from rest_framework import viewsets
from .filters import DriverFilter, LoadFilter, BillingFilter, RateFilter, PreStressBillingLookupFilter, \
    UtilitiesBillingLookupFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # lookup the base std hrs that correspond to the outbound miles
        if serializer.data["delivery_type"] == "UTL":
            base_std_hrs = UtilitiesBillingLookup.objects.get(
                outbound_miles=serializer.data["outbound_miles"]).base_std_hrs
        else:
            base_std_hrs = PreStressBillingLookup.objects.get(
                outbound_miles=serializer.data["outbound_miles"]).base_std_hrs

        # create a default billing record associated with the load
        created_load = Load.objects.get(id=serializer.data["id"])
        Billing.objects.create(load=created_load, base_std_hrs=base_std_hrs)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PreStressBillingLookupViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing pre-stress billing lookup information
    """
    queryset = PreStressBillingLookup.objects.all()
    serializer_class = PreStressBillingLookupSerializer
    filterset_class = PreStressBillingLookupFilter
    pagination_class = PageNumberWithPageSizePagination


class UtilitiesBillingLookupViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing utilities billing lookup information
    """
    queryset = UtilitiesBillingLookup.objects.all()
    serializer_class = UtilitiesBillingLookupSerializer
    filterset_class = UtilitiesBillingLookupFilter
    pagination_class = PageNumberWithPageSizePagination


class BillingViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing all billing information
    """
    queryset = Billing.objects.all()
    serializer_class = BillingSerializer
    filter_class = BillingFilter
    pagination_class = PageNumberWithPageSizePagination


class RateViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing the rate lookup information
    """
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filterset_class = RateFilter
    pagination_class = PageNumberWithPageSizePagination


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

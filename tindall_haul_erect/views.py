from .models import Driver, Load, PreStressBillingLookup, UtilitiesBillingLookup, Billing, Rate, \
    UnloadingTimeLookup, DriverSettlement, SiteSettlement
from .serializers import DriverSerializer, BasicDriverSerializer, LoadSerializer, PreStressBillingLookupSerializer, \
    UtilitiesBillingLookupSerializer, BillingSerializer, RateSerializer, UnloadingTimeLookupSerializer, \
    DriverSettlementSerializer, SiteSettlementSerializer
from rest_framework import viewsets
from .filters import DriverFilter, LoadFilter, BillingFilter, RateFilter, PreStressBillingLookupFilter, \
    UtilitiesBillingLookupFilter, UnloadingTimeLookupFilter, SiteSettlementFilter, DriverSettlementFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from decimal import Decimal
from .utils import calculate_payable_amt, lookup_base_std, lookup_addnl_std_hrs


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
        """
            Description:
            Extending the CreateModelMixin method so that a billing record will automatically be created whenever
            a load is created and is connected to the created load. This is intended to limit the user in the front-end
            from having to create billing records manually, it will give them a default billing record that can be
            updated.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Based on the delivery type lookup the base std hrs that correspond to the outbound miles
        base_std_hrs, _ = lookup_base_std(serializer.data["delivery_type"], serializer.data["outbound_miles"])

        # Based on the delivery type and pieces of the load lookup the addnl std hrs
        addnl_std_hrs = lookup_addnl_std_hrs(serializer.data["delivery_type"], serializer.data["pieces"])

        # create a default billing record associated with the load
        created_load = Load.objects.get(id=serializer.data["id"])
        existing_same_day_load = len(Load.objects.filter(
            driver=created_load.driver, dispatch_date=created_load.dispatch_date
        ))
        # no break if the driver already has existing loads associated with the current load dispatch date
        break_hrs = 0.0 if existing_same_day_load > 1 else 0.5

        Billing.objects.create(
            load=created_load,
            base_std_hrs=base_std_hrs,
            addnl_std_hrs=addnl_std_hrs,
            break_hrs=break_hrs
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        """
            Description:
            Extend the UpdateModelMixin update method, so that if the outbound miles filed is being updated we can
            also update the billing record's base std hrs since the two are linked when the load was created.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        prev_outbound_miles = instance.outbound_miles
        prev_delivery_type = instance.delivery_type
        prev_pieces = instance.pieces
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if prev_outbound_miles != serializer.validated_data["outbound_miles"]:
            # if the outbound miles are being updated then also update the associated billing record's base std hrs
            base_std_hrs, _ = lookup_base_std(
                serializer.validated_data["delivery_type"], serializer.validated_data["outbound_miles"]
            )
            Billing.objects.filter(load=instance).update(base_std_hrs=base_std_hrs)

        if prev_pieces != serializer.validated_data["pieces"] or \
                prev_delivery_type != serializer.validated_data["delivery_type"]:
            # if the pieces or delivery_type fields are being updated then also updat the associated billing record's
            # addnl std hrs
            addnl_std_hrs = lookup_addnl_std_hrs(serializer.data["delivery_type"], serializer.data["pieces"])
            Billing.objects.filter(load=instance).update(addnl_std_hrs=addnl_std_hrs)
            # TODO add logic for if there is a wait time re-calculate as well

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


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

    def update(self, request, *args, **kwargs):
        """
            Description:
            Extend the UpdateModelMixin update method, so that if the update is changing the approved field to
            True then the appropriate site and driver settlements will also be automatically created
            and connected to the updated billing record
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        is_approved = instance.approved
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if not is_approved and serializer.validated_data['approved']:
            # If the current records approved field is False and the updated records approved field is True.
            # Simpler explanation: if we are changing the approval from False to True then calculate the settlements

            # get the site and driver rates
            site_rate = Rate.objects.get(type='site').rate
            driver_rate = Rate.objects.get(type='driver').rate

            # lookup the sites billable amt from the Prestress or Utilities lookup table
            _, base_std_amt = lookup_base_std(instance.load.delivery_type, instance.load.outbound_miles)

            # get the associated load to check if it was canceled or had a layover or is billed to THE
            layover = instance.load.layover
            cancel = instance.load.canceled
            billed_to = instance.load.bill_to

            # TODO add the accessorial charges table to remove the hardcoded values in layover and cancel
            # create the site settlement record
            if billed_to == "THE":
                # THE does not get a site settlement so have the record default to all zeros
                site_settlement = {
                    "load": instance.load,
                    "billing": instance
                }
            else:
                site_settlement = {
                    "load": instance.load,
                    "billing": instance,
                    "base_std": base_std_amt,
                    "addnl_std": calculate_payable_amt(instance.addnl_std_hrs, site_rate),
                    "sec_stop": calculate_payable_amt(instance.sec_stop_hrs, site_rate),
                    "layover": (Decimal("180.00") if layover else Decimal("0.00")),
                    "cancel": (calculate_payable_amt(Decimal("2.0"), site_rate) if cancel else Decimal("0.00")),
                    "wait": calculate_payable_amt(instance.wait_hrs, site_rate)
                }

            SiteSettlement.objects.create(**site_settlement)

            # create the driver settlement record
            driver_settlement = {
                "load": instance.load,
                "billing": instance,
                "base_std": calculate_payable_amt(instance.base_std_hrs, driver_rate),
                "addnl_std": calculate_payable_amt(instance.addnl_std_hrs, driver_rate),
                "sec_stop": calculate_payable_amt(instance.sec_stop_hrs, driver_rate),
                "per_diem": (Decimal("35.00") if layover else Decimal("0.00")),
                "cancel": (calculate_payable_amt(Decimal("2.0"), driver_rate) if cancel else Decimal("0.00")),
                "wait": calculate_payable_amt(instance.wait_hrs, driver_rate),
                "Break": calculate_payable_amt(instance.break_hrs, driver_rate),
                "fringe": calculate_payable_amt(instance.fringe_hrs, driver_rate),
                "tindall_haul_erect_work": calculate_payable_amt(instance.tindall_haul_erect_work_hrs, driver_rate)
            }
            DriverSettlement.objects.create(**driver_settlement)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


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
    filterset_class = UnloadingTimeLookupFilter
    pagination_class = PageNumberWithPageSizePagination


class DriverSettlementViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing the driver settlements
    """
    queryset = DriverSettlement.objects.all()
    serializer_class = DriverSettlementSerializer
    filterset_class = DriverSettlementFilter
    pagination_class = PageNumberWithPageSizePagination


class SiteSettlementViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing the site settlements
    """
    queryset = SiteSettlement.objects.all()
    serializer_class = SiteSettlementSerializer
    filterset_class = SiteSettlementFilter
    pagination_class = PageNumberWithPageSizePagination

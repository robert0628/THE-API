from django_filters import rest_framework as filters
from .models import Driver, Load, Billing, Rate, PreStressBillingLookup, UtilitiesBillingLookup, UnloadingTimeLookup, \
    SiteSettlement, DriverSettlement

from django_property_filter import PropertyFilterSet, PropertyBooleanFilter, PropertyOrderingFilter


# For more information about django_filters see the documentation here
# https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html


class DriverFilter(filters.FilterSet):
    """
    Description:
    A FilterSet for ordering and exact matching the Driver model.
    The Meta class combined with the declared filters automatically handles
    requests with searching, filtering and ordering.

    Example:
        The below url will order the response data by first_name
        url = 'http://192.168.1.40:8000/drivers/?first_name=&last_name=&ordering=first_name'
    """
    first_name = filters.CharFilter(field_name="first_name", lookup_expr="contains")
    hire_date = filters.DateFilter(field_name="hire_date", lookup_expr="exact")

    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('first_name', 'first_name'),
            ('last_name', 'last_name'),
            ('date_of_birth', 'date_of_birth'),
            ('employee_num', 'employee_num'),
            ('tractor_num', 'tractor_num'),
            ('primary_phone_num', 'primary_phone_num'),
            ('email_address', 'email_address'),
            ('hire_date', 'hire_date'),
            ('termination_date', 'termination_date'),
        )
    )

    class Meta:
        model = Driver
        fields = ['first_name', 'last_name']


class LoadFilter(PropertyFilterSet):
    job_name = filters.CharFilter(field_name="job_name", lookup_expr="contains")
    dispatch_date = filters.DateFilter(field_name="dispatch_date", lookup_expr="exact")
    billing__approved = PropertyBooleanFilter(field_name="billing__approved", lookup_expr='exact')

    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('driver', 'driver'),
            ('job_name', 'job_name'),
            ('job_num', 'job_num'),
            ('dispatch_date', 'dispatch_date'),
            ('bill_to', 'bill_to'),
            ('shipment_id', 'shipment_id'),
            ('outbound_miles', 'outbound_miles'),
            ('pieces', 'pieces'),
            ('delivery_type', 'delivery_type'),
            ('canceled', 'canceled'),
            ('layover', 'layover'),
        )
    )

    class Meta:
        model = Load
        fields = ['job_name', 'driver']


class BillingFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('load', 'load'),
            ('base_std_hrs', 'base_std_hrs'),
            ('addnl_std_hrs', 'addnl_std_hrs'),
            ('sec_stop_hrs', 'sec_stop_hrs'),
            ('wait_start_time', 'wait_start_time'),
            ('wait_end_time', 'wait_end_time'),
            ('wait_hrs', 'wait_hrs'),
            ('break_hrs', 'break_hrs'),
            ('fringe_hrs', 'fringe_hrs'),
            ('tindall_haul_erect_work_hrs', 'tindall_haul_erect_work_hrs'),
        )
    )

    class Meta:
        model = Billing
        fields = ['load']


class RateFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('type', 'type'),
            ('rate', 'rate'),
        )
    )

    class Meta:
        model = Rate
        fields = ['type']


class PreStressBillingLookupFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('outbound_miles', 'outbound_miles'),
            ('base_std_hrs', 'base_std_hrs'),
            ('base_std_billable_amt', 'base_std_billable_amt'),
        )
    )

    class Meta:
        model = PreStressBillingLookup
        fields = ['outbound_miles', 'base_std_hrs', 'base_std_billable_amt']


class UtilitiesBillingLookupFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('outbound_miles', 'outbound_miles'),
            ('base_std_hrs', 'base_std_hrs'),
            ('base_std_billable_amt', 'base_std_billable_amt'),
        )
    )

    class Meta:
        model = UtilitiesBillingLookup
        fields = ['outbound_miles', 'base_std_hrs', 'base_std_billable_amt']


class UnloadingTimeLookupFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('delivery_type', 'delivery_type'),
            ('pieces', 'pieces'),
            ('unloading_hrs', 'unloading_hrs'),
            ('addnl_std_hrs', 'addnl_std_hrs'),
        )
    )

    class Meta:
        model = UnloadingTimeLookup
        fields = ['pieces', 'delivery_type', 'unloading_hrs', 'addnl_std_hrs']


class SiteSettlementFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('billing', 'billing'),
            ('base_std', 'base_std'),
            ('addnl_std', 'addnl_std'),
            ('sec_stop', 'sec_stop'),
            ('layover', 'layover'),
            ('wait', 'wait'),
        )
    )

    class Meta:
        model = SiteSettlement
        fields = ['billing']


class DriverSettlementFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('id', 'id'),
            ('billing', 'billing'),
            ('base_std', 'base_std'),
            ('addnl_std', 'addnl_std'),
            ('sec_stop', 'sec_stop'),
            ('per_diem', 'per_diem'),
            ('cancel', 'cancel'),
            ('tindall_haul_erect_work', 'tindall_haul_erect_work'),
        )
    )

    class Meta:
        model = DriverSettlement
        fields = ['billing']

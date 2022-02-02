from django_filters import rest_framework as filters
from .models import Driver, Load

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


class LoadFilter(filters.FilterSet):
    job_name = filters.CharFilter(field_name="job_name", lookup_expr="contains")
    dispatchd_date = filters.DateFilter(field_name="dispatch_date", lookup_expr="exact")

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

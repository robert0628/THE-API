from django_filters import rest_framework as filters
from .models import Driver

# For more information about django_filters see the documentation here
# https://django-filter.readthedocs.io/en/latest/guide/rest_framework.html


class DriverFilter(filters.FilterSet):
    """
    Description:
    A FilterSet for ordering and exact matching the Driver model.
    The Meta class combined with the declared filters automatically handles requests with searches, filters and ordering

    Example:
        The below url will order the response data by first_name
        url = 'http://192.168.1.40:8000/drivers/?first_name=&last_name=&o=first_name'
    """
    ordering = filters.OrderingFilter(
        fields=(
            ('first_name', 'first_name'),
            ('last_name', 'last_name'),
        )
    )

    class Meta:
        model = Driver
        fields = ['first_name', 'last_name']

from django_filters import rest_framework as filters
from .models import Driver


class DriverFilter(filters.FilterSet):
    o = filters.OrderingFilter(
        fields=(
            ('first_name', 'first_name'),
            ('last_name', 'last_name'),
        )
    )

    class Meta:
        model = Driver
        fields = ['first_name', 'last_name']

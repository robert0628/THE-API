from .models import Driver
from .serializers import DriverSerializer
from rest_framework import viewsets


# Create your views here.


class DriverViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing driver information
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer

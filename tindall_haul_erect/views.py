from .models import Driver, Load
from .serializers import DriverSerializer, LoadSerializer
from rest_framework import viewsets


# Create your views here.


class DriverViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing driver information
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer


class LoadViewSet(viewsets.ModelViewSet):
    """
    Description:
    A ViewSet for viewing and editing load information
    """
    queryset = Load.objects.all()
    serializer_class = LoadSerializer

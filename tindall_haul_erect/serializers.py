from rest_framework import serializers
from .models import Driver, Load


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'


class BasicDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = [
            'id',
            'first_name',
            'last_name',
            'date_of_birth',
            'tractor_num',
            'primary_phone_num',
            'email_address',
            'emergency_contact_name',
            'emergency_contact_phone_num'
        ]


class LoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Load
        fields = '__all__'

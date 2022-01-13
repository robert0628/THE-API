from rest_framework import serializers
from .models import Driver, Load, PreStressBillingLookup, UtilitiesBillingLookup


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


class PreStressBillingLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreStressBillingLookup
        fields = '__all__'


class UtilitiesBillingLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UtilitiesBillingLookup
        fields = '__all__'


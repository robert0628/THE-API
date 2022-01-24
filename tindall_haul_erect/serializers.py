from rest_framework import serializers
from .models import Driver, Load, PreStressBillingLookup, UtilitiesBillingLookup, Billing, RateLookup, \
    UnloadingTimeLookup, DriverSettlement, SiteSettlement


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


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = '__all__'


class RateLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateLookup
        fields = '__all__'


class UnloadingTimeLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnloadingTimeLookup
        fields = '__all__'


class DriverSettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverSettlement
        fields = '__all__'


class SiteSettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettlement
        fields = '__all__'


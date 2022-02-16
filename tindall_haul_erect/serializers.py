from rest_framework import serializers
from .models import Driver, Load, PreStressBillingLookup, UtilitiesBillingLookup, Billing, Rate, \
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
        fields = [
            'id',
            'driver',
            'job_name',
            'job_num',
            'dispatch_date',
            'bill_to',
            'shipment_id',
            'outbound_miles',
            'pieces',
            'delivery_type',
            'canceled',
            'layover',
            'billing__approved',
            'billing__id',
            'siteSettlement__id',
            'driverSettlement__id',
        ]


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
        fields = [
            'id',
            'load',
            'base_std_hrs',
            'addnl_std_hrs',
            'sec_stop_hrs',
            'wait_start_time',
            'wait_end_time',
            'wait_hrs',
            'break_hrs',
            'fringe_hrs',
            'tindall_haul_erect_work_hrs',
            'approved',
            'total_hrs',
            'load__driver__id',
            'load__job_name',
            'load__dispatch_date',
        ]


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'


class UnloadingTimeLookupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnloadingTimeLookup
        fields = '__all__'


class DriverSettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverSettlement
        fields = [
            'id',
            'load',
            'billing',
            'base_std',
            'addnl_std',
            'sec_stop',
            'per_diem',
            'cancel',
            'wait',
            'Break',
            'fringe',
            'tindall_haul_erect_work',
            'total',
            'load__driver__id',
            'load__job_name',
            'load__dispatch_date',
        ]


class SiteSettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettlement
        fields = [
            'id',
            'load',
            'billing',
            'base_std',
            'addnl_std',
            'sec_stop',
            'layover',
            'cancel',
            'wait',
            'total',
            'load__bill_to',
            'load__job_name',
            'load__dispatch_date',
        ]



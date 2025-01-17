from django.contrib import admin
from .models import Driver, Load, PreStressBillingLookup, UtilitiesBillingLookup, Billing, Rate, \
    UnloadingTimeLookup, DriverSettlement, SiteSettlement

# Register your models here.
admin.site.register(Driver)
admin.site.register(Load)
admin.site.register(PreStressBillingLookup)
admin.site.register(UtilitiesBillingLookup)
admin.site.register(Billing)
admin.site.register(Rate)
admin.site.register(UnloadingTimeLookup)
admin.site.register(DriverSettlement)
admin.site.register(SiteSettlement)

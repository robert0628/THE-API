from django.contrib import admin
from .models import Driver, Load, PreStressBillingLookup, UtilitiesBillingLookup, Billing

# Register your models here.
admin.site.register(Driver)
admin.site.register(Load)
admin.site.register(PreStressBillingLookup)
admin.site.register(UtilitiesBillingLookup)
admin.site.register(Billing)

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.us.models import USStateField, USZipCodeField, USSocialSecurityNumberField
from django.core.validators import RegexValidator
from datetime import time

# Note: each model is given an id field because react-admin uses this as a default indexer and it is just
#       cleaner to have the rest api respond with an id instead of mapping it out in the front-end


SSN_REGEX = RegexValidator(
    r'^(?!000|.+0{4})(?:\d{3}-\d{2}-\d{4})$',
    message="Invalid SSN, make sure the ssn is valid and use the xxx-xx-xxx format"
)


class Driver(models.Model):
    """
    Description:
    model that represent a truck driver.
    """
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    date_of_birth = models.DateField(blank=False)
    tractor_num = models.CharField(max_length=255, blank=False)
    license_num = models.CharField(max_length=255, blank=False)
    license_state = USStateField(blank=False)
    license_exp = models.DateField(blank=False)
    domicile_location = models.CharField(max_length=255, blank=False)
    social_security_num = USSocialSecurityNumberField(blank=False, validators=[SSN_REGEX], unique=True)
    hire_date = models.DateField(blank=False)
    termination_date = models.DateField(blank=True, null=True)
    employee_num = models.CharField(max_length=255, blank=False, unique=True)
    primary_phone_num = PhoneNumberField(blank=False, unique=True)
    email_address = models.EmailField(max_length=255, blank=False, unique=True)
    home_address = models.CharField(max_length=255, blank=False)
    mailing_address = models.CharField(max_length=255, blank=False)
    city = models.CharField(max_length=100, blank=False)
    state = USStateField(blank=False)
    zip_code = USZipCodeField(blank=False)
    emergency_contact_name = models.CharField(max_length=100, blank=False)
    emergency_contact_phone_num = PhoneNumberField(blank=False)

    def __str__(self):
        return f"Driver: {self.first_name} {self.last_name}"


class Load(models.Model):
    """
    Description:
    model that represent a dispatched load for a trucking delivery
    """
    id = models.BigAutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT)
    job_name = models.CharField(max_length=50, blank=False)
    job_num = models.CharField(max_length=25, blank=False)
    dispatch_date = models.DateField(blank=False)
    bill_to = models.CharField(max_length=10, blank=False)
    shipment_id = models.CharField(max_length=25, blank=False, default="")
    outbound_miles = models.PositiveIntegerField(blank=False, default=0)
    pieces = models.CharField(max_length=10, blank=False, default="0")
    delivery_type = models.CharField(max_length=10, blank=False, default="")
    canceled = models.BooleanField(default=False)
    layover = models.BooleanField(default=False)

    def __str__(self):
        return f"Load {self.job_name} {self.job_num} {self.dispatch_date}"


class PreStressBillingLookup(models.Model):
    """
    Description:
    model that represent a lookup table for pre-stress divisions to decide billable amounts based on outbound miles.

    Usage:
    - Use the bill_to from the Load model to decide if this lookup table should be used (i.e. 100, 400, 700)
    - Use outbound_miles from the Load model to lookup the base standard hours / base standard billable amount
    """
    id = models.BigAutoField(primary_key=True)
    outbound_miles = models.PositiveIntegerField(blank=False, unique=True)
    base_std_hrs = models.DecimalField(max_digits=4, decimal_places=2, blank=False)
    base_std_billable_amt = models.DecimalField(max_digits=6, decimal_places=2, blank=False)


class UtilitiesBillingLookup(models.Model):
    """
    Description:
    model that represent a lookup table for utilities division to decide billable amounts based on outbound miles.

    Usage:
    - Use the bill_to from the Load model to decide if this lookup table should be used (i.e. 200)
    - Use outbound_miles from the Load model to lookup the base standard hours / base standard billable amount
    """
    id = models.BigAutoField(primary_key=True)
    outbound_miles = models.PositiveIntegerField(blank=False, unique=True)
    base_std_hrs = models.DecimalField(max_digits=4, decimal_places=2, blank=False)
    base_std_billable_amt = models.DecimalField(max_digits=6, decimal_places=2, blank=False)


class Billing(models.Model):
    """
    Description:
    model that represent the billable hours for the site and driver.
    """
    id = models.BigAutoField(primary_key=True)
    load = models.OneToOneField(Load, on_delete=models.PROTECT, unique=True)
    base_std_hrs = models.DecimalField(max_digits=4, decimal_places=2, blank=False, default=0.0)
    addnl_std_hrs = models.DecimalField(max_digits=4, decimal_places=2, blank=False, default=0.0)
    sec_stop_hrs = models.DecimalField(max_digits=4, decimal_places=2, blank=False, default=0.0)
    wait_start_time = models.TimeField(blank=False, default=time())
    wait_end_time = models.TimeField(blank=False, default=time())
    wait_hrs = models.DecimalField(max_digits=4, decimal_places=2, blank=False, default=0.0)
    break_hrs = models.DecimalField(max_digits=4, decimal_places=2, blank=False, default=0.0)
    fringe_hrs = models.DecimalField(max_digits=4, decimal_places=2, blank=False, default=0.0)
    tindall_haul_erect_work_hrs = models.DecimalField(max_digits=4, decimal_places=2, blank=False, default=0.0)
    approved = models.BooleanField(default=False)


class RateLookup(models.Model):
    """
    Description:
    model that represent a lookup table for the payable rates of the drivers and plants
    """
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=50, unique=True)
    rate = models.DecimalField(max_digits=6, decimal_places=2, blank=False)


class UnloadingTimeLookup(models.Model):
    """
    Description:
    model that represent a lookup table for the unloading what times based on the delivery type and pieces

    Usage:
        - Using the Billing model, we will need UnloadingTimeLookup data to be able to calculate the wait_hrs
        - wait_hrs = wait_end_time - wait_start_time - unloading_hrs
        - wait_hrs should be rounded to the nearest 1/4 of an hour
    """
    id = models.BigAutoField(primary_key=True)
    delivery_type = models.CharField(max_length=10, blank=False)
    pieces = models.CharField(max_length=10, blank=False)
    unloading_hrs = models.DecimalField(max_digits=4, decimal_places=2, blank=False)
    addnl_std_hrs = models.DecimalField(max_digits=4, decimal_places=2, blank=False)

    class Meta:
        unique_together = ('delivery_type', 'pieces',)


class SiteSettlement(models.Model):
    """
    Description:
    model that represent the settlements for each site

    Usage:
    - Based on who the Load is billed to, use either the PreStressBillingLookup or the UtilitiesBillingLookup
      to lookup the base_std billable amount.
    - For the other fields use the site's rate from the RateLookup table and the billable hours
      to calculate the billable amounts.
    """
    id = models.BigAutoField(primary_key=True)
    billing = models.OneToOneField(Billing, on_delete=models.PROTECT, unique=True)
    base_std = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)
    addnl_std = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)
    sec_stop = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)
    layover = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)
    cancel = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)
    wait = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)


class DriverSettlement(models.Model):
    """
    Description:
    model that represent the settlements for each driver

    Usage:
    - Use driver's rate from the RateLookup table and the billable hours to calculate the billable amounts
    """
    id = models.BigAutoField(primary_key=True)
    billing = models.OneToOneField(Billing, on_delete=models.PROTECT, unique=True)
    base_std = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)
    addnl_std = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)
    sec_stop = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)
    per_diem = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)
    cancel = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)
    wait = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)
    Break = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)
    fringe = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)
    tindall_haul_erect_work = models.DecimalField(max_digits=6, decimal_places=2, blank=False, default=0.0)


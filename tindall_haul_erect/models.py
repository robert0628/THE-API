from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.us.models import USStateField, USZipCodeField, USSocialSecurityNumberField
from django.core.validators import RegexValidator


# Create your models here.
SSN_REGEX = RegexValidator(
    r'^(?!000|.+0{4})(?:\d{3}-\d{2}-\d{4})$',
    message="Invalid SSN, make sure the ssn is valid and use the xxx-xx-xxx format"
)


class Driver(models.Model):
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
    id = models.BigAutoField(primary_key=True)
    driver = models.ForeignKey(Driver, on_delete=models.PROTECT)
    job_name = models.CharField(max_length=50, blank=False)
    job_num = models.CharField(max_length=25, blank=False)
    dispatch_date = models.DateField(blank=False)
    billing_id = models.CharField(max_length=10, blank=False)
    shipment_id = models.CharField(max_length=25, blank=False)
    outbound_miles = models.PositiveIntegerField(blank=True, default=0)
    pieces = models.CharField(max_length=10, blank=True, default="0")
    delivery_type = models.CharField(max_length=10, blank=True, null=True)
    canceled = models.BooleanField(default=False)
    layover = models.BooleanField(default=False)

    def __str__(self):
        return f"Load {self.job_name} {self.job_num} {self.dispatch_date}"




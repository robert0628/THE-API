from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from localflavor.us.models import USStateField, USZipCodeField, USSocialSecurityNumberField


# Create your models here.

class Driver(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    date_of_birth = models.DateField(blank=False)
    tractor_num = models.CharField(max_length=255, blank=False)
    license_num = models.CharField(max_length=255, blank=False)
    license_state = models.CharField(max_length=255, blank=False)
    license_exp = models.DateField(blank=False)
    domicile_location = models.CharField(max_length=255, blank=False)
    social_security_num = USSocialSecurityNumberField(blank=False)
    hire_date = models.DateField(blank=False)
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







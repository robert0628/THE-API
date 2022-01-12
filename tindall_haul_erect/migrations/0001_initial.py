# Generated by Django 4.0.1 on 2022-01-12 18:45

from django.db import migrations, models
import localflavor.us.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('tractor_num', models.CharField(max_length=255)),
                ('license_num', models.CharField(max_length=255)),
                ('license_state', models.CharField(max_length=255)),
                ('license_exp', models.DateField()),
                ('domicile_location', models.CharField(max_length=255)),
                ('social_security_num', localflavor.us.models.USSocialSecurityNumberField(max_length=11)),
                ('hire_date', models.DateField()),
                ('employee_num', models.CharField(max_length=255, unique=True)),
                ('primary_phone_num', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('email_address', models.EmailField(max_length=255, unique=True)),
                ('home_address', models.CharField(max_length=255)),
                ('mailing_address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', localflavor.us.models.USStateField(max_length=2)),
                ('zip_code', localflavor.us.models.USZipCodeField(max_length=10)),
                ('emergency_contact_name', models.CharField(max_length=100)),
                ('emergency_contact_phone_num', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
            ],
        ),
    ]

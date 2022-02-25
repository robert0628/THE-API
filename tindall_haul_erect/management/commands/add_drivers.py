from django.core.management.base import BaseCommand, CommandError
from tindall_haul_erect.models import Driver
import pandas as pd


class Command(BaseCommand):
    """
    Description:
    Bulk insert the drivers data using pandas and django model bulk_create

    Example (terminal):
        $python manage.py add_drivers ./tindall_haul_erect/csv_files/drivers.csv
    """
    help = 'Uses the specified csv file to import drivers into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_name', type=str)

    def handle(self, *args, **options):
        csv_file_name = options['csv_file_name']
        try:
            df_drivers = pd.read_csv(csv_file_name)
            drivers = [
                Driver(
                    first_name=df_drivers.loc[i, "first_name"],
                    last_name=df_drivers.loc[i, "last_name"],
                    date_of_birth=df_drivers.loc[i, "date_of_birth"],
                    tractor_num=df_drivers.loc[i, "tractor_num"],
                    license_num=df_drivers.loc[i, "license_num"],
                    license_state=df_drivers.loc[i, "license_state"],
                    license_exp=df_drivers.loc[i, "license_exp"],
                    domicile_location=df_drivers.loc[i, "domicile_location"],
                    social_security_num=df_drivers.loc[i, "social_security_num"],
                    hire_date=df_drivers.loc[i, "hire_date"],
                    employee_num=df_drivers.loc[i, "employee_num"],
                    primary_phone_num='+'+str(df_drivers.loc[i, "primary_phone_num"]),
                    email_address=df_drivers.loc[i, "email_address"],
                    home_address=df_drivers.loc[i, "home_address"],
                    mailing_address=df_drivers.loc[i, "mailing_address"],
                    city=df_drivers.loc[i, "city"],
                    state=df_drivers.loc[i, "state"],
                    zip_code=df_drivers.loc[i, "zip_code"],
                    emergency_contact_phone_num='+'+str(df_drivers.loc[i, "emergency_contact_phone_num"]),
                )
                for i in df_drivers.index
            ]
            Driver.objects.bulk_create(drivers)
        except Exception as err:
            CommandError('Failed: "%s"' % str(err))

        self.stdout.write(self.style.SUCCESS('Successful imported %s data' % csv_file_name))

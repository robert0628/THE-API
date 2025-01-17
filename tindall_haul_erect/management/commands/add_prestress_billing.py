from django.core.management.base import BaseCommand, CommandError
from tindall_haul_erect.models import PreStressBillingLookup
import pandas as pd


class Command(BaseCommand):
    """
    Description:
    Bulk insert the pre-stress billing lookup data using pandas and django model bulk_create

    Example (terminal):
        $ python manage.py add_prestress_billing ./tindall_haul_erect/csv_files/prestress_billing_lookup_data.csv
    """
    help = 'Uses the specified csv file to import pre-stress billing lookup data into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_name', type=str)

    def handle(self, *args, **options):
        csv_file_name = options['csv_file_name']
        try:
            df_prestress_billings = pd.read_csv(csv_file_name)
            prestress_billings = [
                PreStressBillingLookup(
                    outbound_miles=df_prestress_billings.loc[i, "outbound_miles"],
                    base_std_hrs=df_prestress_billings.loc[i, "base_std_hrs"],
                    base_std_billable_amt=float(df_prestress_billings.loc[i, "base_std_billable_amt"])
                )
                for i in df_prestress_billings.index
            ]
            PreStressBillingLookup.objects.bulk_create(prestress_billings)
        except Exception as err:
            CommandError('Failed: "%s"' % str(err))

        self.stdout.write(self.style.SUCCESS('Successful imported %s data' % csv_file_name))

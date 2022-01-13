from django.core.management.base import BaseCommand, CommandError
from tindall_haul_erect.models import UtilitiesBillingLookup
import pandas as pd


class Command(BaseCommand):
    """
    Description:
    Bulk insert the pre-stress billing lookup data using pandas and django model bulk_create
    """
    help = 'Uses the specified csv file to import pre-stress billing lookup data into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_name', type=str)

    def handle(self, *args, **options):
        csv_file_name = options['csv_file_name']
        try:
            df_utilities_billings = pd.read_csv(csv_file_name)
            utilities_billings = [
                UtilitiesBillingLookup(
                    outbound_miles=df_utilities_billings.loc[i, "outbound_miles"],
                    base_std_hrs=df_utilities_billings.loc[i, "base_std_hrs"],
                    base_std_billable_amt=float(df_utilities_billings.loc[i, "base_std_billable_amt"])
                )
                for i in df_utilities_billings.index
            ]
            UtilitiesBillingLookup.objects.bulk_create(utilities_billings)
        except Exception as err:
            CommandError('Failed: "%s"' % str(err))

        self.stdout.write(self.style.SUCCESS('Successful imported %s data' % csv_file_name))

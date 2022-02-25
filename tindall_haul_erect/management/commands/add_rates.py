from django.core.management.base import BaseCommand, CommandError
from tindall_haul_erect.models import Rate
from decimal import Decimal
import pandas as pd


class Command(BaseCommand):
    """
    Description:
    Bulk insert the rate data using pandas and django model bulk_create

    Example (terminal):
        $ python manage.py add_rates ./tindall_haul_erect/csv_files/rates.csv
    """
    help = 'Uses the specified csv file to import drivers into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_name', type=str)

    def handle(self, *args, **options):
        csv_file_name = options['csv_file_name']
        try:
            df_rates = pd.read_csv(csv_file_name)
            rates = [
                Rate(
                    type=df_rates.loc[i, "type"],
                    rate=Decimal(df_rates.loc[i, "rate"]),
                )
                for i in df_rates.index
            ]
            Rate.objects.bulk_create(rates)
        except Exception as err:
            CommandError('Failed: "%s"' % str(err))

        self.stdout.write(self.style.SUCCESS('Successful imported %s data' % csv_file_name))

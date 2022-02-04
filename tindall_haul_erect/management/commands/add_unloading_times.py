from django.core.management.base import BaseCommand, CommandError
from tindall_haul_erect.models import UnloadingTimeLookup
import pandas as pd


class Command(BaseCommand):
    """
    Description:
    Bulk insert the unloading time lookup data using pandas and django model bulk_create.

    Example (terminal):
        $python manage.py add_unloading_times ./tindall_haul_erect/csv_files/unloading_time_lookup_data.csv
    """
    help = 'Uses the specified csv file to import unloading time lookup data into the database'

    def add_arguments(self, parser):
        parser.add_argument('csv_file_name', type=str)

    def handle(self, *args, **options):
        csv_file_name = options['csv_file_name']
        try:
            df_unloading_times = pd.read_csv(csv_file_name)
            unloading_times = [
                UnloadingTimeLookup(
                    delivery_type=df_unloading_times.loc[i, "delivery_type"],
                    pieces=df_unloading_times.loc[i, "pieces"],
                    unloading_hrs=df_unloading_times.loc[i, "unloading_hrs"],
                    addnl_std_hrs=df_unloading_times.loc[i, "addnl_std_hrs"],
                )
                for i in df_unloading_times.index
            ]
            UnloadingTimeLookup.objects.bulk_create(unloading_times)
        except Exception as err:
            CommandError('Failed: "%s"' % str(err))

        self.stdout.write(self.style.SUCCESS('Successful imported %s data' % csv_file_name))

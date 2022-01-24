# Generated by Django 4.0.1 on 2022-01-21 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tindall_haul_erect', '0011_alter_load_delivery_type_alter_load_shipment_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='RateLookup',
            fields=[
                ('type', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='UnloadingTimeLookup',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('delivery_type', models.CharField(max_length=10)),
                ('pieces', models.CharField(max_length=10)),
                ('unloading_hrs', models.DecimalField(decimal_places=2, max_digits=4)),
                ('addnl_std_hrs', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
    ]

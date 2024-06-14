# Generated by Django 5.0.6 on 2024-06-13 22:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api_common', '0001_initial'),
        ('api_staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='flight',
            field=models.ForeignKey(db_column='flight', on_delete=django.db.models.deletion.CASCADE, to='api_staff.flight'),
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_type',
            field=models.ForeignKey(db_column='booking_type', on_delete=django.db.models.deletion.CASCADE, to='api_common.bookingtype'),
        ),
    ]

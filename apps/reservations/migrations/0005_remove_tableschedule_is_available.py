# Generated by Django 5.1.1 on 2024-12-06 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_reservation_date_created_alter_reservation_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tableschedule',
            name='is_available',
        ),
    ]

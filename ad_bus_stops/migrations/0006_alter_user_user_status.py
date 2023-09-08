# Generated by Django 4.1.1 on 2023-07-17 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ad_bus_stops", "0005_remove_user_agency_staff_user_user_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_status",
            field=models.CharField(
                choices=[("customer", "customer"), ("agency_staff", "agency_staff")],
                default="customer",
                max_length=12,
            ),
        ),
    ]

# Generated by Django 4.1.1 on 2023-07-25 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ad_bus_stops", "0025_app_explorer_delete_study_account"),
    ]

    operations = [
        migrations.AddField(
            model_name="app_explorer",
            name="show_warning",
            field=models.CharField(
                choices=[("yes", "yes"), ("no", "no")], default="yes", max_length=3
            ),
        ),
    ]

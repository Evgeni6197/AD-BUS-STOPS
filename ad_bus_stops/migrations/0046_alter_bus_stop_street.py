# Generated by Django 4.1.1 on 2023-07-29 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ad_bus_stops", "0045_alter_bus_stop_app_explorer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bus_stop", name="street", field=models.CharField(max_length=30),
        ),
    ]
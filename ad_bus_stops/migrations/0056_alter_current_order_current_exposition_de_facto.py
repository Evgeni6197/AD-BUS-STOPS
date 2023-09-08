# Generated by Django 4.1.1 on 2023-08-22 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ad_bus_stops", "0055_alter_bus_stop_staff_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="current_order",
            name="current_exposition_de_facto",
            field=models.CharField(
                choices=[("yes", "yes"), ("no", "no"), ("finished", "finished")],
                default="no",
                max_length=8,
            ),
        ),
    ]
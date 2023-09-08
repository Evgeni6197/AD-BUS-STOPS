# Generated by Django 4.1.1 on 2023-08-21 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "ad_bus_stops",
            "0052_remove_current_order_datetime_of_payment_recording_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="current_order",
            name="datetime_of_ad_removal_de_facto_recording",
        ),
        migrations.RemoveField(
            model_name="current_order",
            name="datetime_of_exposition_de_facto_recording",
        ),
        migrations.RemoveField(
            model_name="orders_archived",
            name="datetime_of_ad_removal_de_facto_recording",
        ),
        migrations.RemoveField(
            model_name="orders_archived",
            name="datetime_of_exposition_de_facto_recording",
        ),
        migrations.RemoveField(
            model_name="orders_archived", name="datetime_of_payment_recording",
        ),
        migrations.RemoveField(model_name="setup_parameters", name="datetime",),
        migrations.AddField(
            model_name="current_order",
            name="date_of_ad_removal_de_facto_recording",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="current_order",
            name="date_of_exposition_de_facto_recording",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="orders_archived",
            name="date_of_ad_removal_de_facto_recording",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="orders_archived",
            name="date_of_exposition_de_facto_recording",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="orders_archived",
            name="date_of_payment_recording",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="setup_parameters",
            name="date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.DeleteModel(name="Letter",),
    ]

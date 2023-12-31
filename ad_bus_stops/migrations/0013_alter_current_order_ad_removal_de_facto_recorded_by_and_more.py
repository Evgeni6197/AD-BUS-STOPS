# Generated by Django 4.1.1 on 2023-07-20 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ad_bus_stops", "0012_current_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="current_order",
            name="ad_removal_de_facto_recorded_by",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ad_removal_de_facto_recorded_orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="current_order",
            name="datetime_of_ad_removal_de_facto_recording",
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name="current_order",
            name="datetime_of_exposition_de_facto_recording",
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name="current_order",
            name="datetime_of_payment_recording",
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name="current_order",
            name="exposition_de_facto_recorded_by",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="exposition_de_facto_recorded_orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="current_order",
            name="payment_recorded_by",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="payment_recorded_orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

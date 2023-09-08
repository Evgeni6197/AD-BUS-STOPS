# Generated by Django 4.1.1 on 2023-07-29 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "ad_bus_stops",
            "0035_remove_current_order_ad_removal_de_facto_recorded_by_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Preemption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "stopId_month_year_explorer",
                    models.CharField(max_length=100, unique=True),
                ),
                (
                    "app_explorer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="preemptions",
                        to="ad_bus_stops.app_explorer",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="preemption",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

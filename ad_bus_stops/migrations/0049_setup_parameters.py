# Generated by Django 4.1.1 on 2023-08-02 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ad_bus_stops", "0048_delete_setup_parameters"),
    ]

    operations = [
        migrations.CreateModel(
            name="SetUp_Parameters",
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
                    "record_status",
                    models.CharField(
                        choices=[("actual", "actual"), ("deprecated", "deprecated")],
                        default="actual",
                        max_length=12,
                    ),
                ),
                ("datetime", models.DateTimeField()),
                ("payment_waiting", models.IntegerField(default=5)),
                ("preparation", models.IntegerField(default=3)),
                ("duration1", models.IntegerField(default=2)),
                ("duration2", models.IntegerField(default=3)),
                ("duration3", models.IntegerField(default=4)),
                ("discount1", models.IntegerField(default=10)),
                ("discount2", models.IntegerField(default=20)),
                ("discount3", models.IntegerField(default=30)),
                ("year", models.IntegerField(default=2025)),
                (
                    "app_explorer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="setup_parameters",
                        to="ad_bus_stops.app_explorer",
                    ),
                ),
                (
                    "staff_member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="set_up_records",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

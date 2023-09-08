# Generated by Django 4.1.1 on 2023-07-20 12:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ad_bus_stops", "0011_preemption"),
    ]

    operations = [
        migrations.CreateModel(
            name="Current_Order",
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
                ("exposition_starts", models.DateField()),
                ("exposition_ends", models.DateField()),
                (
                    "order_status",
                    models.CharField(
                        choices=[
                            ("cart", "cart"),
                            ("payment waiting", "payment waiting"),
                            ("payed exposition waiting", "payed exposition waiting"),
                            (
                                "current exposition de jure",
                                "current exposition de jure",
                            ),
                            ("end of exposition de jure", "end of exposition de jure"),
                        ],
                        default="cart",
                        max_length=26,
                    ),
                ),
                ("total", models.IntegerField(default=0)),
                ("first_booking", models.DateField()),
                (
                    "current_exposition_de_facto",
                    models.CharField(
                        choices=[("yes", "yes"), ("no", "no")],
                        default="no",
                        max_length=3,
                    ),
                ),
                ("datetime_of_payment_recording", models.DateTimeField()),
                ("datetime_of_exposition_de_facto_recording", models.DateTimeField()),
                ("datetime_of_ad_removal_de_facto_recording", models.DateTimeField()),
                (
                    "ad_removal_de_facto_recorded_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ad_removal_de_facto_recorded_orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "exposition_de_facto_recorded_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exposition_de_facto_recorded_orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "payment_recorded_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment_recorded_orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="current_orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
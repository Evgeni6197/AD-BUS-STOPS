# Generated by Django 4.1.1 on 2023-07-20 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("ad_bus_stops", "0020_order_to_remove"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order_to_Place",
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
                    "order",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="ad_bus_stops.current_order",
                    ),
                ),
            ],
        ),
    ]

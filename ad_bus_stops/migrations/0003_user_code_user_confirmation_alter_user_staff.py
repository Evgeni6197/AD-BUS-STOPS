# Generated by Django 4.1.1 on 2023-06-19 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ad_bus_stops", "0002_user_staff"),
    ]

    operations = [
        migrations.AddField(
            model_name="user", name="code", field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="user",
            name="confirmation",
            field=models.CharField(
                choices=[
                    ("confirmed", "confirmed"),
                    ("not_confirmed", "not_confirmed"),
                ],
                default="not_confirmed",
                max_length=13,
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="staff",
            field=models.CharField(
                choices=[("buyer", "buyer"), ("agency_staff", "agency_staff")],
                default="buyer",
                max_length=12,
            ),
        ),
    ]

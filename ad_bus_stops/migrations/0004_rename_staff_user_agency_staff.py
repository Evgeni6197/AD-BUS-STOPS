# Generated by Django 4.1.1 on 2023-06-19 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ad_bus_stops", "0003_user_code_user_confirmation_alter_user_staff"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user", old_name="staff", new_name="agency_staff",
        ),
    ]
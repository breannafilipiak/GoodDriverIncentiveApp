# Generated by Django 3.2.7 on 2021-11-27 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_driver_street_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='driver',
            old_name='sponsor',
            new_name='sponsors',
        ),
    ]
# Generated by Django 3.2.7 on 2021-11-28 00:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_rename_sponsors_driver_sponsor'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Points',
            new_name='Point_Update',
        ),
    ]
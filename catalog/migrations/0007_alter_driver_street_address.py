# Generated by Django 3.2.7 on 2021-11-27 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_rename_apply_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='street_address',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]

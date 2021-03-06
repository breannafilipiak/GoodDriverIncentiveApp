# Generated by Django 3.2.7 on 2021-11-28 01:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0011_auto_20211127_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_total', models.PositiveIntegerField()),
                ('sponsor_org', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='catalog.sponsororg')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='catalog.driver')),
            ],
        ),
    ]

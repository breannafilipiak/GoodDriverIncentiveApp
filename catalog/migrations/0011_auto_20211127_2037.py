# Generated by Django 3.2.7 on 2021-11-28 01:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_rename_points_point_update'),
    ]

    operations = [
        migrations.RenameField(
            model_name='point_update',
            old_name='sponsor_info',
            new_name='updated_by',
        ),
        migrations.RemoveField(
            model_name='point_update',
            name='dollar_value',
        ),
        migrations.RemoveField(
            model_name='point_update',
            name='points_total',
        ),
        migrations.AddField(
            model_name='point_update',
            name='point_change',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='sponsor_account', serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
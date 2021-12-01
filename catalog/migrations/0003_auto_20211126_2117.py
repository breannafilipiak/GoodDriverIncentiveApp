# Generated by Django 3.2.7 on 2021-11-27 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20211126_1629'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='sponsor_org',
            field=models.ManyToManyField(to='catalog.SponsorOrg'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='sponsor',
            field=models.ManyToManyField(blank=True, to='catalog.SponsorOrg'),
        ),
        migrations.CreateModel(
            name='Apply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(blank=True, default=True)),
                ('status', models.BooleanField(blank=True)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('apply_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='apply_to', to='catalog.sponsororg')),
                ('applying', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applying', to='catalog.driver')),
            ],
        ),
    ]
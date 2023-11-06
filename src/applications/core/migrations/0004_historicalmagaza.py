# Generated by Django 4.2.6 on 2023-11-06 17:58

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_auto_20231106_2024'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalMagaza',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('ad', models.CharField(blank=True, max_length=125, null=True, verbose_name='Mağaza Adı')),
                ('enlem', models.FloatField(blank=True, null=True, verbose_name='Mağaza Enlem')),
                ('boylam', models.FloatField(blank=True, null=True, verbose_name='Mağaza Boylam')),
                ('logo', models.TextField(blank=True, max_length=455, null=True, verbose_name='Mağaza Logo')),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='Mağaza Konumu')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical magaza',
                'verbose_name_plural': 'historical magazas',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]

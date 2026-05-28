# Generated migration for inventory app

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vehicle', '0001_initial'),
        ('worklog', '0002_worklog_end_time_worklog_load_type_worklog_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('current_coconuts', models.PositiveIntegerField(default=0)),
                ('current_bags', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GRN',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('receipt_date', models.DateField()),
                ('coconut_count', models.PositiveIntegerField(default=0)),
                ('bag_count', models.PositiveIntegerField(default=0)),
                ('notes', models.TextField(blank=True)),
                ('store', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name='grns',
                    to='inventory.store',
                )),
                ('worklog', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='grns',
                    to='worklog.worklog',
                )),
                ('vehicle', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='grns',
                    to='vehicle.vehicle',
                )),
            ],
            options={
                'ordering': ['-receipt_date', '-created_at'],
            },
        ),
    ]

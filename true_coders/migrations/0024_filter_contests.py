# Generated by Django 2.1.7 on 2020-01-18 23:36

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('true_coders', '0023_auto_20191123_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='filter',
            name='contests',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list),
        ),
    ]

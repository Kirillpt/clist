# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-04 23:44


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_joinrequest_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joinrequest',
            name='event',
        ),
        migrations.RemoveField(
            model_name='joinrequest',
            name='team',
        ),
        migrations.AddField(
            model_name='joinrequest',
            name='registration',
            field=models.ForeignKey(null=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='events.Registration'),
            preserve_default=False,
        ),
    ]

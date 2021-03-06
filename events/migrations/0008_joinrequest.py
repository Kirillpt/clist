# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-04 23:20


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('true_coders', '0009_organization_abbreviation'),
        ('events', '0007_auto_20180204_1901'),
    ]

    operations = [
        migrations.CreateModel(
            name='JoinRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('coder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='true_coders.Coder')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='true_coders.Team')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

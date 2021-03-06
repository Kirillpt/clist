# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-02-02 23:46


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('true_coders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_author_set', to='true_coders.Coder')),
                ('coders', models.ManyToManyField(blank=True, to='true_coders.Coder')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

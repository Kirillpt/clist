# Generated by Django 2.1.7 on 2020-01-17 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_oauth', '0004_auto_20190818_1125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='url_profile',
        ),
    ]

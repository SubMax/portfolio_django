# Generated by Django 3.1.1 on 2020-09-22 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investinfo', '0008_auto_20200922_1214'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data',
            old_name='adj_close',
            new_name='adjclose',
        ),
        migrations.RenameField(
            model_name='data',
            old_name='Datetime',
            new_name='datetime',
        ),
    ]
# Generated by Django 3.1.1 on 2020-09-21 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investinfo', '0005_auto_20200921_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticker',
            name='discription',
        ),
        migrations.AddField(
            model_name='ticker',
            name='description',
            field=models.TextField(default='no descriptions'),
        ),
    ]
# Generated by Django 3.1.1 on 2020-09-19 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investinfo', '0003_discriptionticker'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='discription',
            field=models.TextField(default='no discriptions'),
        ),
        migrations.DeleteModel(
            name='DiscriptionTicker',
        ),
    ]

# Generated by Django 3.1.1 on 2020-09-17 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investinfo', '0002_auto_20200917_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscriptionTicker',
            fields=[
                ('ticker', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='investinfo.ticker')),
                ('discription', models.TextField()),
            ],
        ),
    ]

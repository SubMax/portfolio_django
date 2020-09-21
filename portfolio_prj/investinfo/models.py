from django.db import models


class Ticker(models.Model):
    name = models.CharField(max_length=20)
    ticker = models.CharField(max_length=20, primary_key=True)
    description = models.TextField(default="no descriptions")
    logo_url = models.CharField(max_length=100, default='https://logo.clearbit.com/')


from django.db import models


class Ticker(models.Model):
    name = models.CharField(max_length=20)
    ticker = models.CharField(max_length=20)
    discription = models.TextField(default="no discriptions")


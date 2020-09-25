from django.db import models


class Ticker(models.Model):
    name = models.CharField(max_length=20)
    ticker = models.CharField(max_length=20, primary_key=True)
    description = models.TextField(default="no descriptions")
    logo_url = models.CharField(max_length=100, default='https://logo.clearbit.com/')


class Data(models.Model):
    ticker = models.ForeignKey('Ticker', on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    open = models.DecimalField(max_digits=11, decimal_places=5)
    high = models.DecimalField(max_digits=11, decimal_places=5)
    low = models.DecimalField(max_digits=11, decimal_places=5)
    close = models.DecimalField(max_digits=11, decimal_places=5)
    adjclose = models.DecimalField(max_digits=11, decimal_places=5)
    volume = models.IntegerField()

    # def __str__(self):
    #     return 's%' % self.datetime

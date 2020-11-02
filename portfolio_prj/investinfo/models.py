from django.db import models
from django.shortcuts import Http404
from .stockdata import get_info_data


class TickerManager(models.Manager):
    def available_list(self):
        try:
            avail_lst = super(TickerManager, self).get_queryset().order_by('symbol')
        except self.model.DoesNotExist:
            avail_lst = None
        return list(avail_lst)

    def information(self, ticker_name):
        try:
            ticker_info = super(TickerManager, self).filter(symbol=ticker_name).values()
            ticker_info = ticker_info.get()
        except self.model.DoesNotExist:
            ticker_info = get_info_data(tickername=ticker_name)
            if ticker_info:
                new_ticker = Ticker(longName=ticker_info.get('longName'),
                                    symbol=ticker_info.get('symbol'),
                                    longBusinessSummary=ticker_info.get('longBusinessSummary'),
                                    logo_url=ticker_info.get('logo_url'),
                                    )
                new_ticker.save()
            else:
                raise Http404
        return ticker_info


class Ticker(models.Model):
    longName = models.CharField(max_length=20)
    symbol = models.CharField(max_length=20, primary_key=True)
    longBusinessSummary = models.TextField(default="no descriptions")
    logo_url = models.CharField(max_length=100,
                                default='https://logo.clearbit.com/')
    available = TickerManager()


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

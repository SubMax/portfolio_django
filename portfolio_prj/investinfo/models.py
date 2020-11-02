from django.db import models
from django.shortcuts import Http404
from datetime import datetime, timedelta, timezone
from .stockdata import get_info_data, fetch_data


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


class DataManager(models.Manager):
    DICT_PERIOD = {
        '1d': 1,
        '5d': 5,
        '1mo': 30,
        '3mo': 90,
        '6mo': 180,
        '1y': 365,
        '2y': 730,
        '5y': 365 * 5,
        '10y': 365 * 10,
        'ytd': 365 * 10,
        'max': 40 * 365
    }
    DICT_INTERVAL = {
        '1m': 1,
        '2m': 2,
        '5m': 5,
        '15m': 15,
        '30m': 30,
        '60m': 60,
        '90m': 90,
        '1h': 60,
        '1d': 24 * 60,
        '5d': 24 * 60 * 5,
        '1wk': 24 * 60 * 7,
        '1mo': 24 * 60 * 30,
        '3mo': 24 * 60 * 90
    }

    def query_set_to_dict(self, data, qs, interval):
        global DICT_INTERVAL
        data['date'] = [i[0] for i in qs.values_list(
            'datetime')][::self.DICT_INTERVAL.get(interval, 1)]
        data['adjclose'] = [float(i[0]) for i in qs.values_list(
            'adjclose')][::self.DICT_INTERVAL.get(interval, 1)]
        return data

    def stock_period_data(self, ticker_name, period, interval):
        data = {
            'date': None,
            'adjclose': None,
        }

        if period and interval:
            point_date = datetime.now() - timedelta(days=self.DICT_PERIOD.get(period, 1),
                                                    hours=datetime.now().hour,
                                                    minutes=datetime.now().minute,
                                                    seconds=datetime.now().second,
                                                    microseconds=datetime.now().microsecond)
            query_data = super(DataManager, self).get_queryset().filter(ticker_id=ticker_name,
                                                   datetime__gte=point_date).order_by('datetime').distinct()
            data = self.query_set_to_dict(data, query_data, interval)

        if not data['date'] and not data['adjclose']:
            fetch_data(ticker_name=ticker_name, period=period, interval=interval)
            query_data = super(DataManager, self).get_queryset().filter(ticker_id=ticker_name,
                                                   datetime__gte=point_date).order_by('datetime').distinct()
            data = self.query_set_to_dict(data, query_data, interval)

        return data

    def start_end_data(self):
        pass


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
    get_data = DataManager()

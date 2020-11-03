from django.shortcuts import render, redirect, Http404
from .models import Ticker, Data
from .forms import TickerForm, DateForm, PeriodForm, IntervalForm
from .stockdata import fetch_data
from datetime import datetime, timedelta, timezone
import re

DICT_VALID_PERIOD = {
    '1d': '1d',
    '5d': '5d',
    '1mo': '1mo',
    '3mo': '3mo',
    '6mo': '6mo',
    '1y': '1y',
    '2y': '2y',
    '5y': '5y',
    '10y': '10y',
    'ytd': 'ytd',
    'max': 'ytd'
}
DICT_VALID_INTERVAL = {
    '1m': '1m',
    '2m': '2m',
    '5m': '5m',
    '15m': '15m',
    '30m': '30m',
    '60m': '60m',
    '90m': '90m',
    '1h': '1h',
    '1d': '1d',
    '5d': '5d',
    '1wk': '1wk',
    '1mo': '1mo',
    '3mo': '3mo'
}



def index(request):
    """
    Основная страница приложения.
    :param request:
    :return:
    """

    if request.method == "POST":
        request_ticker = request.POST.get('symbol', 'DIS').upper()
        return redirect('ticker_info', ticker=request_ticker)

    list_ticker = Ticker.available.available_list()
    ticker_form = TickerForm()

    context = {
        'title': "Список тикеров",
        'list_ticker': list_ticker,
        'tickerform': ticker_form
    }
    return render(request, 'investinfo/list_ticker.html', context=context)


def about(request):
    """
    Страница About.
    :param request:
    :return:
    """
    return render(request, 'investinfo/about.html')


def description_ticker(request, ticker):
    """
    Страница с описанием.
    :param request:
    :param ticker: наименование тикера
    :return:
    """
    information = Ticker.available.information(ticker_name=ticker)

    context = {
        'title': information.get('symbol'),
        'name': information.get('longName'),
        'description': information.get('longBusinessSummary'),
        'logo_url': information.get('logo_url'),
    }
    return render(request, 'investinfo/ticker.html', context=context)


def stock_data_ticker(request,
                      ticker,
                      text,
                      period=None,
                      interval=None,
                      **kwargs):
    """
    Информация о ценах.
    :param request:
    :param ticker: наименование тикера
    :param text:
    :param period: запрашиваемы период
    :param interval: запрашиваемый интервал
    :param kwargs:
    :return:
    """

    if request.method == 'GET':
        info = Ticker.available.information(ticker_name=ticker)

        if period and interval and kwargs.__len__() < 3:
            data = Data.get_data.stock_period_data(ticker_name=ticker,
                                                   period=DICT_VALID_PERIOD.get(period, '1d'),
                                                   interval=DICT_VALID_INTERVAL.get(interval, '1m'))
        elif kwargs.__len__() == 6:
            start = datetime(year=kwargs.get('ystart'),
                             month=kwargs.get('mstart'),
                             day=kwargs.get('dstart'),
                             tzinfo=timezone(-timedelta(hours=4)))
            end = datetime(year=kwargs.get('yend'),
                           month=kwargs.get('mend'),
                           day=kwargs.get('dend') + 1,
                           tzinfo=timezone(-timedelta(hours=4)))
            data = Data.get_data.start_end_data(ticker_name=ticker,
                                                start=start,
                                                end=end,
                                                interval=DICT_VALID_INTERVAL.get(interval, '1m'))

    if request.method == 'POST':
        if request.POST.get('period') and request.POST.get('interval'):
            return redirect('chart_period',
                            ticker=ticker,
                            text=text,
                            period=request.POST.get('period'),
                            interval=request.POST.get('interval'))

        elif request.POST.get('start') and request.POST.get('end') and request.POST.get('interval'):
            ystart, mstart, dstart = date_to_lst(
                request.POST.get('start'), key='int')
            yend, mend, dend = date_to_lst(
                request.POST.get('end'), key='int')
            interval = request.POST.get('interval')
            return redirect('chart_date',
                            ticker=ticker,
                            text=text,
                            ystart=ystart,
                            mstart=mstart,
                            dstart=dstart,
                            yend=yend,
                            mend=mend,
                            dend=dend,
                            interval=interval)
        else:
            raise Http404

    date_form = DateForm()
    period_form = PeriodForm()
    interval_form = IntervalForm()
    context = {
        'title': ticker,
        'period': period,
        'interval': interval,
        'logo_url': info.get('logo_url'),
        'date': [d.strftime('%d-%m-%y %H:%M') for d in data['date']],
        'adjclose': data['adjclose'],
        'dateform': date_form,
        'periodform': period_form,
        'intervalform': interval_form
    }
    return render(request, 'investinfo/stockdata.html', context=context)


def lst_to_date(lst):
    """
    :param lst: list [гггг, мм, дд]
    :return: date гггг-мм-дд
    """
    year, month, day = lst
    date = '-'.join([str(year), str(month), str(day)])
    pattern = r'\d\d\d\d-\d\d-\d\d'
    result = re.search(pattern, date)
    if result:
        return result.string
    return result


def date_to_lst(date, key='str'):
    """
    :param key:
    :param date: str
    :return: list
    """
    lst = None
    if key == 'str':
        lst = str.split(date, sep='-')
    elif key == 'int':
        lst = [int(d) for d in str.split(date, sep='-')]

    return lst

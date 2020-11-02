from django.shortcuts import render, redirect, Http404
from .models import Ticker, Data
from .forms import TickerForm, DateForm, PeriodForm, IntervalForm
from .stockdata import get_info_data, fetchdata
from datetime import datetime, timedelta, timezone
import re

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
    'ytd': 10,
    'max': 40*365
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
    '5d': 1,
    '1wk': 2,
    '1mo': 3,
    '3mo': 4
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
            data = get_period_stock_data(ticker, period, interval)
            if not data['date'] and not data['adjclose'] and text:
                fetchdata(tickername=ticker, period=period, interval=interval)
                data = get_period_stock_data(ticker, period, interval)
        elif kwargs.__len__() == 6:
            start = datetime(year=kwargs.get('ystart'),
                             month=kwargs.get('mstart'),
                             day=kwargs.get('dstart'),
                             tzinfo=timezone(-timedelta(hours=4)))
            end = datetime(year=kwargs.get('yend'),
                           month=kwargs.get('mend'),
                           day=kwargs.get('dend') + 1,
                           tzinfo=timezone(-timedelta(hours=4)))
            data = get_start_end_stock_data(ticker, start, end, interval)

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


def get_period_stock_data(ticker, period='1d', interval='1m'):
    """
    Получение данных за период.
    :param ticker: наименование тикера
    :param period: запрашиваемы период
    :param interval: запрашиваемый интервал
    :return:
    """
    data = {'date': None,
            'adjclose': None}
    global DICT_PERIOD
    global DICT_INTERVAL

    if period and interval:
        point_date = datetime.now() - timedelta(days=DICT_PERIOD.get(period),
                                                hours=datetime.now().hour,
                                                minutes=datetime.now().minute,
                                                seconds=datetime.now().second,
                                                microseconds=datetime.now().microsecond)
        qdata = Data.objects.all().filter(ticker_id=ticker,
                                          datetime__gte=point_date).order_by('datetime').distinct()
        data['date'] = [i[0] for i in qdata.values_list(
            'datetime')][::DICT_INTERVAL.get(interval)]
        data['adjclose'] = [float(i[0]) for i in qdata.values_list(
            'adjclose')][::DICT_INTERVAL.get(interval)]
    return data


def get_start_end_stock_data(ticker, start, end, interval='1m', data=None):
    """
    Получение данных в промежуток
    :param ticker: наименование тикера
    :param start: начало промежутка
    :param end: конец промежутка
    :param interval: запрашиваемый интервал
    :param data:
    :return:
    """
    global DICT_INTERVAL

    if start > end:
        start, end = end, start

    if not data:
        data = {'date': None,
                'adjclose': None}
        query_data = Data.objects.all().filter(ticker_id=ticker,
                                               datetime__gte=start,
                                               datetime__lte=end).order_by('datetime').distinct()

    data['date'] = [i[0] for i in query_data.values_list(
        'datetime')][::DICT_INTERVAL.get(interval)]
    data['adjclose'] = [float(i[0]) for i in query_data.values_list(
        'adjclose')][::DICT_INTERVAL.get(interval)]  # Danger

    if not data['date'] and not data['adjclose']:
        try:
            fetchdata(tickername=ticker, start=start, end=end, interval=interval)
            query_data = Data.objects.all().filter(ticker_id=ticker,
                                                   datetime__gte=start,
                                                   datetime__lte=end).order_by('datetime').distinct()

            data['date'] = [i[0] for i in query_data.values_list(
                'datetime')][::DICT_INTERVAL.get(interval)]
            data['adjclose'] = [float(i[0]) for i in query_data.values_list(
                'adjclose')][::DICT_INTERVAL.get(interval)]
        except:
            return data

    if data['date'] and data['adjclose']:
        first = data['date'][0]
        last = data['date'][-1]

        if first > start:
            try:
                fetchdata(tickername=ticker, start=start, end=first, interval=interval)
            except:
                print('pre_query_data: None')
            pre_query_data = Data.objects.all().filter(ticker_id=ticker,
                                                       datetime__gte=start,
                                                       datetime__lte=first).order_by('datetime').distinct()

        if last < end:
            try:
                fetchdata(tickername=ticker, start=last, end=end, interval=interval)

            except:
                print('post_query_data: None')
            post_query_data = Data.objects.all().filter(ticker_id=ticker,
                                                        datetime__gte=last,
                                                        datetime__lte=end).order_by('datetime').distinct()

        all_query_data = pre_query_data | query_data | post_query_data

        data['date'] = [i[0] for i in all_query_data.values_list(
            'datetime')][::DICT_INTERVAL.get(interval)]
        data['adjclose'] = [float(i[0]) for i in all_query_data.values_list(
            'adjclose')][::DICT_INTERVAL.get(interval)]

    return data


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

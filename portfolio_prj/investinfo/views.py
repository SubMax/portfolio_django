from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from .models import Ticker, Data
from .forms import TickerForm, DateForm, MySetForm
from .stockData import getstockdata, fetchdata
from datetime import datetime, timedelta
import re


def index(request):
    """
    метод для генерации основной страници приложения
    :param request: запрос
    :return:
    """

    if request.method == "POST":
        request_ticker = request.POST['ticker'].upper()
        try:
            if Ticker.objects.get(ticker=request_ticker):
                return redirect('ticker_info', ticker=request_ticker)
        except Ticker.DoesNotExist:
            print("DoseNotExist")
            data = getstockdata(request_ticker)
            new_ticker = Ticker(name=data[1],
                                ticker=data[0],
                                description=data[2],
                                logo_url=data[3])
            new_ticker.save()
            return descriptionticker(request, request_ticker)

    list_ticker = Ticker.objects.all().order_by('ticker')
    tickerform = TickerForm()
    trushlabel = tickerform.fields.get('ticker')  # удаляем ненужную подпись
    trushlabel.label = ''

    context = {
        'title': "Список тикеров",
        'list_ticker': list_ticker,
        'tickerform': tickerform
    }
    return render(request, 'investinfo/list_ticker.html', context=context)


def descriptionticker(request, ticker, text=None, **kwargs):
    """
    Метод для отоброжения информации о инструменте
    :param text: chart
    :param ystart: гггг
    :param mstart: мм
    :param dstart: дд
    :param yend: гггг
    :param mend: мм
    :param dend: дд
    :param period: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    :param interval: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    :param request: запрос
    :param ticker: краткое название биржевого инструмента
    :return:
    """
    info = Ticker.objects.get(ticker=ticker)

    data = get_period_stock_data(ticker, kwargs.get('period'), kwargs.get('interval'))

    dateform = DateForm()
    context = {
        'title': info.ticker,
        'name': info.name,
        'description': info.description,
        'logo_url': info.logo_url,
        'date': data['date'],
        'adjclose': data['adjclose'],
        'dateform': dateform
    }

    if text == "chart":
        return render(request, 'investinfo/stockdata.html', context=context)
    elif text:
        raise Http404
    return render(request, 'investinfo/ticker.html', context=context)


def get_period_stock_data(ticker, period='1d', interval='1m'):
    data = dict()
    DICT_PERIOD = {
        '1d': 1,
        '5d': 5,
        '1mo': 30,
        '3mo': 90,
        '6mo': 180,
        '1y': 365,
        '2y': 730,
        '5y': 365*5,
        '10y': 365*10,
        'ytd': 10,
        'max': 11
    }
    poin_date = datetime.now() - timedelta(days=DICT_PERIOD[period])
    qdata = Data.objects.all().filter(ticker_id=ticker, datetime__gte=poin_date).order_by('datetime').distinct()
    data['date'] = [i[0] for i in qdata.values_list('datetime')]
    data['adjclose'] = [float(i[0]) for i in qdata.values_list('adjclose')]
    return data

def stock_data_js(request, ticker, date=[0, 1, 2, 3]):
    # ToDo реализовать labels: [{% for d in date %}'{{d}}',{% endfor %}]
    return JsonResponse(data={
        'ticker': ticker
    })


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


def date_to_lst(date):
    """
    :param date: str
    :return: list
    """
    lst = str.split(date, sep='-')

    return lst

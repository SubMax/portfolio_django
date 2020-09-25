from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from .models import Ticker, Data
from .forms import TickerForm
from .stockData import getStockData, fetchData
import re


def index(request):
    """
    метод для генерации основной страници приложения
    :param request: запрос
    :return:
    """

    if request.method == "POST":
        request_ticker = request.POST['ticker'].upper()

        if Ticker.objects.get(ticker=request_ticker):
            return redirect('ticker_info', ticker=request_ticker)

        data = getStockData(request_ticker)
        new_ticker = Ticker(name=data[1], ticker=data[0], description=data[2], logo_url=data[3])
        new_ticker.save()
        return descriptionTicker(request, request_ticker)

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


def descriptionTicker(request, ticker, text=None, ystart='', mstart='', dstart='', yend='', mend='', dend='', period='',
                      interval=''):
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
    if text and ystart:
        start = checkDate(ystart, mstart, dstart)
        end = checkDate(yend, mend, dend)
        if start and end:
            fetchData(ticker, start, end, interval=interval)

    info = Ticker.objects.get(ticker=ticker)
    qdata = Data.objects.all().filter(ticker_id=ticker)
    date = [i[0] for i in qdata.values_list('datetime')]
    adjclose = [float(i[0]) for i in qdata.values_list('adjclose')]
    context = {
        'title': info.ticker,
        'name': info.name,
        'description': info.description,
        'logo_url': info.logo_url,
        'date': date,
        'adjclose': adjclose  # stockDataJS(request, ticker)
    }
    if text == "chart":
        return render(request, 'investinfo/stockdata.html', context=context)
    elif text:
        raise Http404
    return render(request, 'investinfo/ticker.html', context=context)


def stockDataJS(request, ticker, date=[0, 1, 2, 3]):
    return JsonResponse(data={
        'ticker': ticker
    })


def checkDate(year, month, day):
    date = '-'.join([str(year), str(month), str(day)])
    pattern = r'\d\d\d\d-\d\d-\d\d'
    result = re.search(pattern, date)
    if result:
        return result.string
    return result

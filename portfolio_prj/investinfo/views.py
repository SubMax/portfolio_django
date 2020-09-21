from django.shortcuts import render
from .models import Ticker
from .forms import TicketForm
from .stockData import getStockData


def index(request):
    """
    метод для генерации основной страници приложения
    :param request: запрос
    :return:
    """

    if request.method == "POST":
        data = getStockData(request.POST['ticker'])
        new_ticker = Ticker(name=data[1], ticker=data[0], description=data[2], logo_url=data[3])
        new_ticker.save()
        return descriptionTicker(request, data[0])

    list_ticker = Ticker.objects.all().order_by('ticker')
    tickerform = TicketForm()
    trushlabel = tickerform.fields.get('ticker')  # удаляем ненужную подпись
    trushlabel.label = ''

    context = {
        'title': "Список тикеров",
        'list_ticker': list_ticker,
        'tickerform': tickerform
    }
    return render(request, 'investinfo/list_ticker.html', context=context)


def descriptionTicker(request, ticker):
    """
    Метод для отоброжения информации о инструменте
    :param request: запрос
    :param ticker: краткое название биржевого инструмента
    :return:
    """

    qticker = Ticker.objects.get(ticker=ticker)
    context = {
        'title': qticker.ticker,
        'name': qticker.name,
        'description': qticker.description,
        'logo_url': qticker.logo_url
    }
    return render(request, 'investinfo/ticker.html', context=context)

from django.shortcuts import render
from .models import Ticker


def index(request):
    list_ticker = Ticker.objects.all().order_by('ticker')
    context = {
        'title': "Список тикеров",
        'list_ticker': list_ticker
    }
    return render(request, 'investinfo/list_ticker.html', context=context)

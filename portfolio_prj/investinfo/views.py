from django.shortcuts import render
from .models import Ticker
from django.views.generic import DetailView


class InfoTicker(DetailView):
    model = Ticker
    template_name = 'investinfo/ticker.html'
    context_object_name = 'ticker'


def index(request):
    list_ticker = Ticker.objects.all().order_by('ticker')
    context = {
        'title': "Список тикеров",
        'list_ticker': list_ticker
    }
    return render(request, 'investinfo/list_ticker.html', context=context)


# def discriptionTicker(request, ticname):
#     discription = Ticker.objects.get(ticname)
#     context = {
#         'title': discription.ticker,
#         'discription': discription.discription
#     }
#     return render(request, 'investinfo/ticker.html', context=context)

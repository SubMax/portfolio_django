from .models import Ticker
from django.forms import ModelForm, Form, TextInput, DateField, formset_factory
from datetime import date, timedelta


class TickerForm(ModelForm):
    class Meta:
        model = Ticker
        fields = ['ticker']
        labels = {'ticker': ''}
        widgets = {
            'ticker': TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "Название тикер",
                'aria-describedby': "Введите название тикера"
            })
        }


class DateForm(Form):
    today = date.today()
    yesterday = today - timedelta(days=1)
    start = DateField(widget=TextInput(attrs={'type': "date", 'value': yesterday, 'max': today}), label='')
    end = DateField(widget=TextInput(attrs={'type': "date", 'value': today, 'max': today}), label='')
    accept = DateField(widget=TextInput(attrs={
        'type': "submit",
        'class': "btn btn-secondary",
        'value': "Применить"
    }), label='')


class PeriodForm(Form):
    one_day = DateField(widget=TextInput(attrs={'type': "submit",
                                                'class': "btn btn-secondary",
                                                'href': "/investinfo/{{ title }}/chart/1d/1m",
                                                'value': "1d"
                                                }),
                        label='')
    five_day = DateField(widget=TextInput(attrs={'type': "submit",
                                                 'class': "btn btn-secondary",
                                                 'href': "/investinfo/{{ title }}/chart/1d/1m",
                                                 'value': "5d"}),
                         label='')
    one_month = DateField(widget=TextInput(attrs={'type': "submit", 'class': "btn btn-secondary", 'value': "1m"}),
                          label='')
    three_month = DateField(widget=TextInput(attrs={'type': "submit", 'class': "btn btn-secondary", 'value': "3m"}),
                            label='')
    six_month = DateField(widget=TextInput(attrs={'type': "submit", 'class': "btn btn-secondary", 'value': "6m"}),
                          label='')
    ytd = DateField(widget=TextInput(attrs={'type': "submit", 'class': "btn btn-secondary", 'value': "ytd"}),
                    label='')
    one_year = DateField(widget=TextInput(attrs={'type': "submit", 'class': "btn btn-secondary", 'value': "1y"}),
                         label='')
    two_year = DateField(widget=TextInput(attrs={'type': "submit", 'class': "btn btn-secondary", 'value': "2y"}),
                         label='')
    five_year = DateField(widget=TextInput(attrs={'type': "submit", 'class': "btn btn-secondary", 'value': "5y"}),
                          label='')
    max = DateField(widget=TextInput(attrs={'type': "submit", 'class': "btn btn-secondary", 'value': "max"}),
                    label='')
    buttons = [one_day, five_day]

from .models import Ticker
from django.forms import ModelForm, Form, TextInput, DateField, ChoiceField
from datetime import date, timedelta


class TickerForm(ModelForm):
    class Meta:
        model = Ticker
        fields = ['ticker']
        labels = {'ticker': ''}
        widgets = {
            'ticker': TextInput(attrs={
                'class': "mdl-textfield__input",
                'type': "text",
                'placeholder': "Ввдите название тикер"
            })
        }


class DateForm(Form):
    today = date.today()
    yesterday = today - timedelta(days=1)
    start = DateField(widget=TextInput(attrs={'type': "date", 'value': yesterday, 'max': today}), label='')
    end = DateField(widget=TextInput(attrs={'type': "date", 'value': today, 'max': today}), label='')
    accept = DateField(widget=TextInput(attrs={
        'type': "submit",
        'class': "mdl-button mdl-js-button mdl-button--raised",
        'value': "Ok",
        # 'style': "height: 10px"
    }), label='')


class PeriodForm(Form):
    tuple_period = ((p, p) for p in "1d,5d,1mo,3mo,6mo".split(','))
    period = ChoiceField(choices=tuple_period, label='')
    ok = DateField(widget=TextInput(attrs={
        'type': "submit",
        'class': "mdl-button mdl-js-button mdl-button--raised",
        'onClick': "dataSelect(this.form)",
        'value': "Ok"
    }), label='')


class IntervalForm(Form):
    tuple_interval = ((p, p) for p in "1m,2m,5m,15m,30m,60m".split(','))
    interval = ChoiceField(choices=tuple_interval, label='')
    ok = DateField(widget=TextInput(attrs={
        'type': "submit",
        'class': "mdl-button mdl-js-button mdl-button--raised",
        'onClick': "dataSelect(this.form)",
        'value': "Ok"
    }), label='')

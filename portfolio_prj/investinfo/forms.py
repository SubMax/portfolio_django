from .models import Ticker
from django.forms import ModelForm, Form, TextInput, DateField, SelectDateWidget, CharField


class TickerForm(ModelForm):
    class Meta:
        model = Ticker
        fields = ['ticker']
        label = '1'
        widgets = {
            'ticker': TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "Название тикер",
                'aria-describedby': "Введите название тикера"
            })
        }


class DateForm(Form):
    start = DateField(widget=TextInput(attrs={'type': "date"}), label='')
    end = DateField(widget=TextInput(attrs={'type': "date"}), label='')

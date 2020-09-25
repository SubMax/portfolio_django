from .models import Ticker
from django.forms import ModelForm, TextInput


class TickerForm(ModelForm):
    class Meta:
        model = Ticker
        fields = ['ticker']
        widgets = {
            'ticker': TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "Название тикер",
                'aria-describedby': "Введите название тикера"
            })
        }

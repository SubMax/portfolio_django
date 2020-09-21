from .models import Ticker, DiscriptionTicker
from django.forms import ModelForm, TextInput, Textarea


class TicketForm(ModelForm):
    class Meta:
        model = Ticker
        fields = ['ticker', 'name']
        widgets = {
            'ticker': TextInput(attrs={
                'class': "form-control",
                'placeholder': "result"
            }),
            'name': TextInput(attrs={
                'class': "form-control",
                'placeholder': "result"
            })
        }


class DiscriptionTickerForm(ModelForm):
    class Meta:
        model = DiscriptionTicker
        fields = ['ticker', 'discription']
        widgets = {
            'ticker': TextInput(attrs={
                'class': "form-control"
            }),
            'discription': Textarea(attrs={
                'class': "form-control"
            })
        }

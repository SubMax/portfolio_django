from .models import Ticket
from django.forms import ModelForm, TextInput


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
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

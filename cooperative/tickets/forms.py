from django import forms
from .models import Ticket

class BuyTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['trip', 'seat_number']
        widgets = {
            'trip': forms.HiddenInput()
}
    
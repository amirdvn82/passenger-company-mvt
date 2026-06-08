from django import forms

class BuyTicketForm(forms.Form):
    trip_id = forms.IntegerField()
    seat_number = forms.IntegerField(max_value=1)
    
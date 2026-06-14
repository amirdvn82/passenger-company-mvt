from django import forms
from .models import Trip
from cities.models import CityDistance

class TripCreateForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["vehicle", "origin", "destination", "departure_time", "capacity"]
        widgets = {"departure_time": forms.DateTimeInput(attrs={"type": "datetime-local"})}

    def clean(self):
        cleaned_data = super().clean()
        origin = cleaned_data.get("origin")
        destination = cleaned_data.get("destination")
        vehicle = cleaned_data.get("vehicle")
        capacity = cleaned_data.get("capacity")

        if origin and destination:
            try:
                CityDistance.objects.get(origin=origin, destination=destination)
            except CityDistance.DoesNotExist:
                raise forms.ValidationError(
                    f"The distance between '{origin.name}' and '{destination.name}' is not defined. Please add it in the admin panel.")



        if vehicle and capacity and capacity > vehicle.capacity:
                raise forms.ValidationError(
                    f"Trip capacity ({capacity}) cannot exceed vehicle capacity ({vehicle.capacity}).")
        return cleaned_data
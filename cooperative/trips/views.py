from django.shortcuts import render
from .models import Trip


def trip_list_view(request):
    trips = Trip.objects.all()
    return render(request, "trips/trip-list.html", {"trips": trips})

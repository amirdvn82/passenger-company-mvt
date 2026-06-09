from django.shortcuts import render
from .models import Trip
from django.contrib.auth.decorators import login_required
from accounts.models import DriverProfile

def trip_list_view(request):
    trips = Trip.objects.all()
    return render(request, "trips/trip-list.html", {"trips": trips})



@login_required
def driver_dashboard_view(request):

    driver = DriverProfile.objects.get(user=request.user)
    trips = driver.trips.all()
    return render(request, "trips/driver-dashboard.html", {"trips": trips})
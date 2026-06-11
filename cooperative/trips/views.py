from django.shortcuts import render, redirect
from .models import Trip
from django.contrib.auth.decorators import login_required
from accounts.models import DriverProfile
from django.contrib import messages

def trip_list_view(request):
    trips = Trip.objects.all()
    return render(request, "trips/trip-list.html", {"trips": trips})



@login_required
def driver_dashboard_view(request):
    
    try:
        driver = DriverProfile.objects.get(user=request.user)
        
    except DriverProfile.DoesNotExist:
        messages.error(request, 'You are not registered as a driver.')
        return redirect('trips:trip-list')
    trips = driver.trips.all()
    return render(request, "trips/driver-dashboard.html", {"trips": trips})
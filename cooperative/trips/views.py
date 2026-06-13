from django.shortcuts import render, redirect, get_object_or_404
from .models import Trip
from django.contrib.auth.decorators import login_required
from accounts.models import DriverProfile
from django.contrib import messages
from tickets.models import Ticket
from django.db.models import Count, Q

def trip_list_view(request):
    trips = Trip.objects.all()
    return render(request, "trips/trip-list.html", {"trips": trips})



def driver_dashboard_view(request):
    if not hasattr(request.user, 'driver_profile'):
        return render(request, 'error.html', {'message': 'You are not a driver.'})

    driver_profile = request.user.driver_profile

    trips = Trip.objects.filter(driver=driver_profile).annotate(tickets_sold=Count('tickets', filter=Q(tickets__status=Ticket.Status.ACTIVE))).order_by('-departure_time')

    total_earnings = 0
    for trip in trips:
        trip.revenue = trip.tickets_sold * trip.price
        total_earnings += trip.revenue

    context = {'trips': trips, 'total_earnings': total_earnings,}
    return render(request, 'trips/driver-dashboard.html', context)


@login_required
def trip_passengers_view(request, trip_id):

    trip = get_object_or_404(Trip, id=trip_id)
    if not hasattr(request.user, 'driver_profile') or trip.driver != request.user.driver_profile:

        if not request.user.is_staff:
            return render(request, 'error.html', {'message': 'You do not have access to this page'})
    
    tickets = Ticket.objects.filter(trip=trip, status=Ticket.Status.ACTIVE).select_related('user')
    return render(request, 'trips/trip-passengers.html', {'trip': trip, 'tickets': tickets})
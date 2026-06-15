from django.shortcuts import render, redirect, get_object_or_404
from .models import Trip
from django.contrib.auth.decorators import login_required
from accounts.models import DriverProfile
from django.contrib import messages
from tickets.models import Ticket
from django.db.models import Count, Q
from .forms import TripCreateForm
from cities.models import City
from django.utils import timezone


def trip_list_view(request):
    if request.user.is_authenticated and hasattr(request.user, 'driver_profile'):
        if not request.user.driver_profile.is_approved:
            return render(request, 'trips/waiting-approval.html')
    trips = Trip.objects.filter(status=Trip.Status.APPROVED)
    return render(request, "trips/trip-list.html", {"trips": trips})



def driver_dashboard_view(request):
    if not hasattr(request.user, 'driver_profile'):
        return render(request, 'error.html', {'message': 'You are not a driver.'})

    driver_profile = request.user.driver_profile
    
    if not driver_profile.is_approved:

        messages.warning(request, "Your driver account is waiting for admin approval.")

        return redirect('trips:trip-list')
    
    trips = Trip.objects.filter(driver=driver_profile).annotate(tickets_sold=Count('tickets', filter=Q(tickets__status=Ticket.Status.ACTIVE))).order_by('-departure_time')


    trips_data=[]
    total_earnings = 0
    for trip in trips:
        
        revenue = trip.tickets_sold * trip.price
        total_earnings += revenue
        
        trips_data.append({'trip': trip, 'tickets_sold': trip.tickets_sold, 'revenue': revenue })

    context = {'trips_data': trips_data, 'total_earnings': total_earnings,}
    return render(request, 'trips/driver-dashboard.html', context)


@login_required
def trip_passengers_view(request, trip_id):

    trip = get_object_or_404(Trip, id=trip_id)
    if not hasattr(request.user, 'driver_profile') or trip.driver != request.user.driver_profile:

        if not request.user.is_staff:
            return render(request, 'error.html', {'message': 'You do not have access to this page'})
    
    tickets = Ticket.objects.filter(trip=trip, status=Ticket.Status.ACTIVE).select_related('user')
    return render(request, 'trips/trip-passengers.html', {'trip': trip, 'tickets': tickets})


@login_required
def create_trip_view(request):

    if not hasattr(request.user, "driver_profile"):
        return render(request, "error.html", {"message": "You are not a driver."})

    driver_profile = request.user.driver_profile

    if not driver_profile.is_approved:
        messages.error(request, "Your driver account is not approved.")
        return redirect("trips:trip-list")

    if request.method == "POST":

        form = TripCreateForm(request.POST)

        form.fields["vehicle"].queryset = (driver_profile.vehicles.all())

        if form.is_valid():

            trip = form.save(commit=False)

            trip.driver = driver_profile

            trip.status = Trip.Status.PENDING

            trip.save()

            messages.success(request, "Trip created successfully and waiting for admin approval.")

            return redirect("trips:driver-dashboard")

    else:

        form = TripCreateForm()

        form.fields["vehicle"].queryset = (driver_profile.vehicles.all())

    return render(request, "trips/create-trip.html", {"form": form})




def home_view(request):
    if request.user.is_authenticated and hasattr(request.user, 'driver_profile'):
        if not request.user.driver_profile.is_approved:
            return render(request, 'trips/waiting-approval.html', {'message': 'Your driving account is awaiting admin review'})


    origin_id = request.GET.get('origin')
    destination_id = request.GET.get('destination')
    date_str = request.GET.get('date')
    trips = Trip.objects.filter(status=Trip.Status.APPROVED, departure_time__date__gte=timezone.now().date()).select_related('origin', 'destination', 'driver__user', 'vehicle')
    
    if origin_id:
        trips = trips.filter(origin_id=origin_id)
    if destination_id:
        trips = trips.filter(destination_id=destination_id)
    if date_str:
        trips = trips.filter(departure_time__date=date_str)
    
    cities = City.objects.all().order_by('name')

    context = {
        'trips': trips,
        'cities': cities,
        'selected_origin': origin_id,
        'selected_destination': destination_id,
        'selected_date': date_str,
    }

    return render(request, 'home.html', context)


def tripـdetail_view(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id)
    return render(request, 'trips/trip-detail.html', {'trip': trip})
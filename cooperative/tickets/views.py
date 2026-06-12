from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BuyTicketForm
from .services import TicketService, TicketPurchaseError
from trips.models import Trip
from .models import Ticket
from django.utils import timezone
from django.contrib import messages


@login_required
def buy_ticket_view(request, trip_id):
   
    trip = get_object_or_404(Trip, id=trip_id)
   
    if request.method == "POST":
        form = BuyTicketForm(request.POST)

        if form.is_valid():
            #trip_id = form.cleaned_data["trip_id"]
            seat_number = form.cleaned_data["seat_number"]

            #trip = Trip.objects.get(id=trip_id)

            try:
                TicketService.buy_ticket(user=request.user, trip=trip, seat_number=seat_number)
                return redirect("ticket-success")

            except TicketPurchaseError as e:
                form.add_error(None, str(e))

    else:
        form = BuyTicketForm(initial={"trip_id": trip_id})

    return render(request, "tickets/buy-ticket.html", {"form": form, "trip": trip})

@login_required
def ticket_success_view(request):
    return render(request, "tickets/success.html")


@login_required
def my_tickets_view(request):
    
    tickets = Ticket.objects.filter(user=request.user).select_related('trip', 'trip__origin', 'trip__destination').order_by('-created_date')
    now = timezone.now()
    return render(request, 'tickets/my-tickets.html', {'tickets': tickets, 'now': now})

@login_required
def cancel_ticket_view(request, ticket_id):
    if request.method == 'POST':
        try:
            TicketService.cancel_ticket(ticket_id=ticket_id, user=request.user)
            messages.success(request, 'The ticket has been successfully cancelled and the funds have been returned to your wallet.')
        except (ValueError, PermissionError, TicketPurchaseError) as e:
            messages.error(request, str(e))
    return redirect('tickets:my-tickets')

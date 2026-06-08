from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import BuyTicketForm
from .services import TicketService, TicketPurchaseError
from trips.models import Trip


@login_required
def buy_ticket_view(request):

    if request.method == "POST":
        form = BuyTicketForm(request.POST)

        if form.is_valid():
            trip_id = form.cleaned_data["trip_id"]
            seat_number = form.cleaned_data["seat_number"]

            trip = Trip.objects.get(id=trip_id)

            try:
                ticket = TicketService.buy_ticket(user=request.user, trip=trip, seat_number=seat_number)
                return redirect("ticket_success")

            except TicketPurchaseError as e:
                form.add_error(None, str(e))

    else:
        form = BuyTicketForm()

    return render(request, "tickets/buy_ticket.html", {"form": form})

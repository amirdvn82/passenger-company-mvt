from django.db import transaction
from wallets.services import WalletService, InsufficientBalanceError
from .models import Ticket
from trips.models import Trip


class TicketPurchaseError(Exception):
    pass


class TicketService:

    @staticmethod
    @transaction.atomic
    def buy_ticket(*, user, trip, seat_number):

        if trip.status != Trip.Status.APPROVED:
            raise TicketPurchaseError("Trip is not approved")

        if seat_number < 1 or seat_number > trip.capacity:
            raise TicketPurchaseError("Invalid seat number")

        if trip.tickets.count() >= trip.capacity:
            raise TicketPurchaseError("Trip is full")

        if Ticket.objects.filter(trip=trip, seat_number=seat_number).exists():
            raise TicketPurchaseError("Seat already reserved")

        price = trip.price

        if price > 0:
            try:
                WalletService.withdraw(
                    user=user,
                    amount=price,
                    description=f"Ticket purchase for trip #{trip.id}"
                )
            except InsufficientBalanceError:
                raise TicketPurchaseError("Insufficient balance")

        ticket = Ticket.objects.create(
            user=user,
            trip=trip,
            seat_number=seat_number,
            status=Ticket.Status.RESERVED
        )

        return ticket

from django.db import transaction, IntegrityError
from wallets.services import WalletService, InsufficientBalanceError
from .models import Ticket
from trips.models import Trip
from django.utils import timezone
from django.contrib import messages
from decimal import Decimal
from django.utils import timezone
from cities.models import SystemSetting



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

        if trip.tickets.filter(status=Ticket.Status.ACTIVE).count() >= trip.capacity:
            raise TicketPurchaseError("Trip is full")

        if Ticket.objects.filter(trip=trip, seat_number=seat_number, status=Ticket.Status.ACTIVE,).exists():
            raise TicketPurchaseError("Seat already reserved")

        if Ticket.objects.filter(user=user, trip=trip, status=Ticket.Status.ACTIVE,).exists():
            raise TicketPurchaseError("You already have a ticket for this trip")

        if trip.departure_time <= timezone.now():
            raise TicketPurchaseError('The time for departure has passed.')


        price = trip.price

        if price > 0:
            try:
                
                WalletService.withdraw(user=user, amount=price, description=f"Ticket purchase for trip #{trip.id}")
            
            except InsufficientBalanceError:
                
                raise TicketPurchaseError("Insufficient balance")
            
            try:
                
                ticket = Ticket.objects.create(user=user, trip=trip, seat_number=seat_number, status=Ticket.Status.ACTIVE)
            
            except IntegrityError:
                
                raise TicketPurchaseError("Seat already reserved")

        
        return ticket

    @staticmethod
    @transaction.atomic
    def cancel_ticket(ticket_id, user): 
        try:

            ticket = Ticket.objects.select_for_update().get(id=ticket_id, user=user, status='ACTIVE')
            
            ticket.status = 'CANCELLED'
            ticket.save()
            

        except Ticket.DoesNotExist:
            raise TicketPurchaseError("The requested ticket could not be found or has already been canceled.")

        if ticket.trip.departure_time <= timezone.now():
            raise TicketPurchaseError("Cannot cancel ticket after departure time.")    

        setting = SystemSetting.objects.first()
        penalty_percent = (setting.refund_percentage if setting else Decimal("10"))
        

        price = Decimal(ticket.trip.price)
        refund_amount = price * (Decimal("100") - penalty_percent) / Decimal("100")

        if refund_amount > 0:
            WalletService.refund(user=ticket.user, amount=refund_amount, description=f"Refund for cancelled ticket #{ticket.id} (penalty {penalty_percent}%)")

        ticket.status = Ticket.Status.CANCELLED
        ticket.save(update_fields=["status"])

        return ticket
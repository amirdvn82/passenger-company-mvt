from decimal import Decimal
from django.db import transaction
from django.db.models import F
from .models import Wallet, WalletTransaction
from tickets.models import Ticket
from trips.models import Trip
from django.utils import timezone

class InsufficientBalanceError(Exception):
    pass
class TicketPurchaseError(Exception):
    pass

class WalletService:

    @staticmethod
    @transaction.atomic
    def deposit(user, amount: Decimal, description: str = ""):
        """
        Increase user's wallet balance.
        """

        amount = Decimal(amount)

        if amount <= 0:
            return 

        wallet, _ = Wallet.objects.select_for_update().get_or_create(user=user)

        wallet.balance = F("balance") + amount
        wallet.save(update_fields=["balance"])
        wallet.refresh_from_db()

        WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type=WalletTransaction.TransactionType.DEPOSIT,
            description=description,
        )

        return wallet.balance

    @staticmethod
    @transaction.atomic
    def withdraw(user, amount: Decimal, description: str = ""):
        """
        Decrease user's wallet balance safely.
        """

        amount = Decimal(amount)

        # ✅ اگر مبلغ صفر یا منفی بود هیچ کاری نکن
        if amount <= 0:
            return

        wallet, _ = Wallet.objects.select_for_update().get_or_create(user=user)

        # ✅ جلوگیری از منفی شدن موجودی
        if wallet.balance < amount:
            raise InsufficientBalanceError("Insufficient balance")

        wallet.balance = F("balance") - amount
        wallet.save(update_fields=["balance"])
        wallet.refresh_from_db()

        WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type=WalletTransaction.TransactionType.WITHDRAW,
            description=description,
        )

        return wallet.balance
    
    @staticmethod
    @transaction.atomic
    def refund(user, amount: Decimal, description: str = ""):
        if amount <= 0:
            raise TicketPurchaseError("Refund amount must be positive")
        wallet, _ = Wallet.objects.select_for_update().get_or_create(user=user)
        wallet.balance += amount
        wallet.save(update_fields=["balance"])
        WalletTransaction.objects.create(
            wallet=wallet,
            amount=amount,
            transaction_type=WalletTransaction.TransactionType.REFUND,
            description=description
        )
        return wallet.balance
    
    @staticmethod
    @transaction.atomic
    def cancel_ticket(*, ticket_id: int, user):
        from cities.models import SystemSetting  # برای دریافت درصد جریمه

        try:
            ticket = Ticket.objects.select_for_update().get(id=ticket_id)
        except Ticket.DoesNotExist:
            raise TicketPurchaseError("Ticket not found")

        # بررسی دسترسی: فقط صاحب بلیط یا ادمین
        if ticket.user != user and not user.is_staff:
            raise TicketPurchaseError("You cannot cancel this ticket")

        if ticket.status != Ticket.Status.ACTIVE:
            raise TicketPurchaseError("Only active tickets can be cancelled")

        if ticket.trip.departure_time <= timezone.now():
            raise TicketPurchaseError("Cannot cancel ticket after departure time")

        # درصد جریمه
        setting = SystemSetting.objects.first()
        refund_percent = setting.refund_percentage if setting else Decimal('10.0')
        refund_amount = ticket.trip.price * (Decimal('100') - refund_percent) / Decimal('100')

        # برگشت وجه
        WalletService.refund(
            user=ticket.user,
            amount=refund_amount,
            description=f"Refund for cancelled ticket #{ticket.id} (penalty {refund_percent}%)"
        )
    
        # تغییر وضعیت بلیط
        ticket.status = Ticket.Status.CANCELLED
        ticket.save(update_fields=['status'])

    @staticmethod
    @transaction.atomic
    def mark_as_used(*, ticket_id: int, user):
        """Marks a ticket as used."""
        try:
            ticket = Ticket.objects.select_for_update().get(id=ticket_id)
        except Ticket.DoesNotExist:
            raise TicketPurchaseError("Ticket not found")

        # Basic checks: User should own the ticket or be staff, and ticket must be active
        if ticket.user != user and not user.is_staff:
            raise TicketPurchaseError("You do not have permission to mark this ticket as used")
            
        if ticket.status != Ticket.Status.ACTIVE:
            raise TicketPurchaseError("Ticket is not active")
        
        
        ticket.status = Ticket.Status.USED
        ticket.save(update_fields=['status'])
        
        return ticket
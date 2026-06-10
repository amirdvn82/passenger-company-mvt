from decimal import Decimal
from django.db import transaction
from django.db.models import F
from .models import Wallet, WalletTransaction


class InsufficientBalanceError(Exception):
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
            raise ValueError("Refund amount must be positive")
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
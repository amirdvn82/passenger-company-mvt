from decimal import Decimal

from django.db import transaction

from .models import Wallet, WalletTransaction


class InsufficientBalanceError(Exception):
    pass


class WalletService:

    @staticmethod
    @transaction.atomic
    def deposit(user, amount: Decimal, description: str = ""):

        if amount <= 0:
            raise ValueError("Deposit amount must be positive")

        wallet, _ = Wallet.objects.select_for_update().get_or_create(user=user)

        wallet.balance += amount

        wallet.save(update_fields=["balance"])

        WalletTransaction.objects.create(
            wallet=wallet, amount=amount, transaction_type=WalletTransaction.TransactionType.DEPOSIT, description=description)

        return wallet.balance

    @staticmethod
    @transaction.atomic
    def withdraw(user, amount: Decimal, description: str = ""):

        if amount <= 0:
            raise ValueError("Withdraw amount must be positive")

        wallet, _ = Wallet.objects.select_for_update().get_or_create(user=user)

        if wallet.balance < amount:
            raise InsufficientBalanceError("Insufficient balance")

        wallet.balance -= amount

        wallet.save(update_fields=["balance"])

        WalletTransaction.objects.create(wallet=wallet, amount=amount, transaction_type=WalletTransaction.TransactionType.WITHDRAW, description=description)

        return wallet.balance
from django.db import models
from django.conf import settings


class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.PositiveBigIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Wallet'


class WalletTransaction(models.Model):

    class TransactionType(models.TextChoices):
        DEPOSIT = 'DEPOSIT', 'Deposit'
        WITHDRAW = 'WITHDRAW', 'Withdraw'
        REFUND = 'REFUND', 'Refund'
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')

    amount = models.DecimalField(max_digits=12, decimal_places=0)
    transaction_type = models.CharField( max_length=20, choices=TransactionType.choices)

    created_date = models.DateTimeField(auto_now_add=True)

    description = models.CharField(max_length=255, blank=True)

    

    def __str__(self):
        return f"{self.wallet.user.username} - {self.get_transaction_type_display()} - {self.amount}"


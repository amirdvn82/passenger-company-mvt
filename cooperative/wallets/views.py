from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import WalletTransaction
from .services import WalletService

@login_required
def wallet_dashboard(request):
    wallet = request.user.wallet
    return render(request, 'wallets/wallet-dashboard.html', {'wallet': wallet})

@login_required
def transaction_list(request):
    transactions = WalletTransaction.objects.filter(wallet__user=request.user).order_by('-created_date')
    return render(request, 'wallets/transaction-list.html', {'transactions': transactions})

@login_required
def charge_wallet(request):
    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                raise ValueError
            WalletService.deposit(request.user, amount, description="Wallet recharge by user")
            messages.success(request, f"{amount:,.0f} Dollars added to your wallet.")
            return redirect('wallets:wallet-dashboard')
        except (ValueError, TypeError):
            messages.error(request, "Invalid amount. Please enter a positive number.")
    return render(request, 'wallets/wallet-charge.html')
from django.urls import path
from . import views

app_name = 'wallets'

urlpatterns = [
    path('', views.wallet_dashboard, name='wallet-dashboard'),
    path('transactions/', views.transaction_list, name='transaction-list'),
    path('charge/', views.charge_wallet, name='wallet-charge'),
]
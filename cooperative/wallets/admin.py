from django.contrib import admin
from .models import Wallet, WalletTransaction

class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'created_date', 'updated_date')
    search_fields = ('user__username',)
    readonly_fields = ('balance',)

admin.site.register(Wallet, WalletAdmin)

class WalletTransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'amount', 'transaction_type', 'created_date', 'description')
    list_filter = ('transaction_type', 'created_date')
    search_fields = ('wallet__user__username',)

admin.site.register(WalletTransaction)
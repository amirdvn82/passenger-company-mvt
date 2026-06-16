from django.contrib import admin
from .models import Ticket

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'trip', 'seat_number', 'status', 'created_date')
    list_filter = ('status', 'created_date')
    search_fields = ('user__username', 'trip__origin__name', 'trip__destination__name')

admin.site.register(Ticket, TicketAdmin)

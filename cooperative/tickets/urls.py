from django.urls import path
from .views import *

app_name = 'tickets'

urlpatterns = [
    path("buy/<int:trip_id>", buy_ticket_view, name="buy-ticket"),
    path("success/", ticket_success_view, name="ticket-success"),
    path('my-tickets/', my_tickets_view, name='my-tickets'),
    path('cancel/<int:ticket_id>/', cancel_ticket_view, name='cancel_ticket'),

]

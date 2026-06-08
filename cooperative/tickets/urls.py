from django.urls import path
from .views import *

urlpatterns = [
    path("buy/", buy_ticket_view, name="buy-ticket"),
    path("success/", ticket_success_view, name="ticket-success"),

]

from django.urls import path
from .views import buy_ticket_view

urlpatterns = [
    path("buy/", buy_ticket_view, name="buy_ticket"),
]

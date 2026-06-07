from django.db import models
from django.conf import settings
from trips.models import Trip


class Ticket(models.Model):

    class Status(models.TextChoices):
        RESERVED = "RESERVED", "Reserved"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tickets")

    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="tickets")

    seat_count = models.PositiveIntegerField(default=1)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RESERVED)

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.trip}"

from django.db import models
from accounts.models import DriverProfile, Vehicle
from cities.models import City
from django.db.models import Sum


class Trip(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='trips')

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    origin = models.ForeignKey(City, on_delete=models.CASCADE, related_name='trip_origins')

    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name='trip_destinations')

    departure_time = models.DateTimeField()

    capacity = models.PositiveIntegerField()

    price = models.PositiveIntegerField()

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.origin} → {self.destination}'


    def reserved_seats(self):
        result = self.tickets.aggregate(total=Sum("seat_count"))
        return result["total"] or 0

    def remaining_capacity(self):
        return self.capacity - self.reserved_seats()

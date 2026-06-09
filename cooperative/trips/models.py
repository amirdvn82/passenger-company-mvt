from django.db import models
from accounts.models import DriverProfile, Vehicle
from cities.models import City
from cities.services import calculate_trip_price, calculate_travel_time_minutes
from django.apps import apps   

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

    price = models.PositiveIntegerField(blank=True, null=True)

    travel_time_minutes = models.PositiveIntegerField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    created_date = models.DateTimeField(auto_now_add=True)



    def save(self, *args, **kwargs):

        if self.origin == self.destination:
            raise ValueError("Origin and destination cannot be the same")

        if self.capacity > self.vehicle.capacity:
            raise ValueError("Trip capacity cannot exceed vehicle capacity")

        if self.origin_id and self.destination_id:
            if self.origin_id == self.destination_id:
                raise ValueError("Origin and destination cannot be the same")

            if self.price is None:
                self.price = calculate_trip_price(self.origin, self.destination)

            if self.travel_time_minutes is None:
                self.travel_time_minutes = calculate_travel_time_minutes(self.origin, self.destination)

        super().save(*args, **kwargs)

    
    def __str__(self):
        return f'{self.origin} → {self.destination}'


    def reserved_seats(self):
        Ticket = apps.get_model('tickets', 'Ticket') 
        return self.tickets.filter(status=Ticket.Status.RESERVED).count()
    
    
    @property
    def remaining_capacity(self):
        return self.capacity - self.reserved_seats()
    
    @property
    def sold_seats(self):
        return self.reserved_seats()
    
    @property
    def revenue(self):

        return self.sold_seats * self.price
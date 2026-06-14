from django.db import models
from accounts.models import DriverProfile, Vehicle
from cities.models import City, CityDistance
from cities.services import calculate_trip_price, calculate_travel_time_minutes
from django.apps import apps   
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


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
            try:
                if not self.price:
                    self.price = calculate_trip_price(self.origin, self.destination)
                if not self.travel_time_minutes:
                    self.travel_time_minutes = calculate_travel_time_minutes(self.origin, self.destination)
            
            except CityDistance.DoesNotExist:
                raise ValueError(f"Distance between {self.origin.name} and {self.destination.name} is not defined. Please add it in admin panel.")
    
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f'{self.origin} → {self.destination}'


    def reserved_seats(self):
        Ticket = apps.get_model('tickets', 'Ticket') 
        return self.tickets.filter(status=Ticket.Status.ACTIVE).count()
    
    
    @property
    def remaining_capacity(self):
        return self.capacity - self.reserved_seats()
    
    @property
    def sold_seats(self):
        return self.reserved_seats()
    
    @property
    def revenue(self):

        return self.sold_seats * self.price
    
    def create_trip_permissions():
        content_type = ContentType.objects.get_for_model(Trip)
        #Permission to view driver dashboard
        Permission.objects.get_or_create(codename='view_driver_dashboard', name='Can view driver dashboard', content_type=content_type)
        #Permission to manage trips by admin
        Permission.objects.get_or_create(codename='manage_trip', name='Can manage trips', content_type=content_type)
        #Other permissions for regular user trips
        Permission.objects.get_or_create(codename='view_trip', name='Can view trips', content_type=content_type)
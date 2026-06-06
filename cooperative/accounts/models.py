from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    class Role(models.TextChoices):
        USER = 'USER', 'User'
        DRIVER = 'DRIVER', 'Driver'
        ADMIN = 'ADMIN', 'Admin'
    phone_number = models.CharField(max_length=11, unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    is_verified = models.BooleanField(default=False) 
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    
    def __str__(self):
        return self.username
    
class DriverProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="driver_profile")

    national_code = models.CharField(max_length=10, unique=True)
    license_number = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Driver"

class Vehicle(models.Model):

    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name="vehicles")

    plate_number = models.CharField(max_length=15, unique=True)
    car_model = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.car_model} - {self.plate_number}"

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
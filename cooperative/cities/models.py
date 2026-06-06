from django.db import models

class City(models.Model):

    name = models.CharField(max_length=100, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class CityDistance(models.Model):

    origin = models.ForeignKey(City, on_delete=models.CASCADE, related_name="origin_routes")

    destination = models.ForeignKey(City, on_delete=models.CASCADE, related_name="destination_routes")

    distance_km = models.PositiveIntegerField()

    base_time_minutes = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.origin} → {self.destination}"

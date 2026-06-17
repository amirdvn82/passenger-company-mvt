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


    class Meta:
        unique_together = ("origin", "destination")
    
    def __str__(self):
        return f"{self.origin} → {self.destination}"

class SystemSetting(models.Model):

    price_per_km = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
        help_text="Price per kilometer"
    )
    time_per_km = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
        help_text="Estimated time per kilometer (minutes)"
    )


    refund_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=10.00,
        help_text="Ticket cancellation penalty percentage is 10% "
    )

    class Meta:
        verbose_name = "System Settings"
        verbose_name_plural = "System Settings"

    def __str__(self):
        return f"Settings: Price={self.price_per_km}, Time={self.time_per_km}, Penalty={self.refund_percentage}%"

    def save(self, *args, **kwargs):
        
        if not self.pk and SystemSetting.objects.exists():
            return
        return super().save(*args, **kwargs)

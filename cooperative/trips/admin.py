from django.contrib import admin
from .models import Trip


class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'origin', 'destination', 'departure_time', 'driver', 'status', 'price')
    list_filter = ('status', 'departure_time')
    actions = ['approve_trips', 'reject_trips']

    def approve_trips(self, request, queryset):
        updated = queryset.update(status=Trip.Status.APPROVED)
        self.message_user(request, f"{updated} Trip is approved.")
    approve_trips.short_description = "Confirm selected trips"
    def reject_trips(self, request, queryset):
        updated = queryset.update(status=Trip.Status.REJECTED)
        self.message_user(request, f"{updated} The trip was rejected.")
    reject_trips.short_description = "Reject selected trips"

admin.site.register(Trip, TripAdmin)
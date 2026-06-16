from django.contrib import admin

from .models import User, DriverProfile, Vehicle

class CustomUserAdmin(User):
    inlines = [DriverProfile]
    list_display = ('username', 'phone_number', 'first_name', 'last_name', 'role', 'is_verified', 'is_active')
    list_filter = ('role', 'is_verified', 'is_active')
    search_fields = ('username', 'phone_number', 'first_name', 'last_name')
    actions = ['approve_drivers']
    def approve_drivers(self, request, queryset):
        for user in queryset.filter(role=User.Role.DRIVER):
            user.is_verified = True
            user.save()
            if hasattr(user, 'driver_profile'):
                user.driver_profile.is_approved = True
                user.driver_profile.save()
        self.message_user(request, 'Selected drivers confirmed.')
    approve_drivers.short_description = 'Confirm selected drivers'

admin.site.register(User, CustomUserAdmin)


class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'national_code', 'license_number', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('user__username', 'national_code', 'license_number')

admin.site.register(DriverProfile, DriverProfileAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'car_model', 'capacity', 'driver')
    list_filter = ('driver',)
    search_fields = ('plate_number', 'car_model')

admin.site.register(Vehicle, VehicleAdmin)
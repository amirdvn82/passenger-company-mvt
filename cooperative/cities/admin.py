from django.contrib import admin
from .models import City, CityDistance, SystemSetting

class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(City, CityAdmin)


class CityDistanceAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'distance_km', 'base_time_minutes')
    list_filter = ('origin', 'destination')
    search_fields = ('origin__name', 'destination__name')

admin.site.register(CityDistance, CityDistanceAdmin)


class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('price_per_km', 'time_per_km', 'refund_percentage')

    fieldsets = (
        ('Price Settings', {'fields': ('price_per_km',)}),
        ('Time Settings', {'fields': ('time_per_km',)}),
        ('Penalty Settings ', {'fields': ('refund_percentage',)}),
    )

    def has_add_permission(self, request):
        return not SystemSetting.objects.exists()

admin.site.register(SystemSetting, SystemSettingAdmin)
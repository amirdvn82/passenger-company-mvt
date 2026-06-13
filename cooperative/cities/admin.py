from django.contrib import admin
from .models import City, CityDistance, SystemSetting

class SystemSettingAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return not SystemSetting.objects.exists()


admin.site.register(City)
admin.site.register(CityDistance)
admin.site.register(SystemSetting)

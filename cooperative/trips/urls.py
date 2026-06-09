from django.urls import path
from .views import *

urlpatterns = [

        path("", trip_list_view, name="trip-list"),
        path("driver-dashboard/", driver_dashboard_view, name="driver-dashboard"),
]

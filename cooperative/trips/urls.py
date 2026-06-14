from django.urls import path
from .views import *

app_name = 'trips'
urlpatterns = [

        path("trip-list", trip_list_view, name="trip-list"),
        path("driver-dashboard/", driver_dashboard_view, name="driver-dashboard"),
        path("trip/<int:trip_id>/passengers/", trip_passengers_view, name="trip-passengers"),
]

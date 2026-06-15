from django.urls import path
from .views import *

app_name = 'trips'
urlpatterns = [

        path("trip-list", trip_list_view, name="trip-list"),
        path("driver-dashboard/", driver_dashboard_view, name="driver-dashboard"),
        path("trip/<int:trip_id>/passengers/", trip_passengers_view, name="trip-passengers"),
        path("create/", create_trip_view, name="create-trip"),
        path('<int:trip_id>/', tripـdetail_view, name='trip-detail'),
        path('waiting-approval/', waiting_approval_view, name='waiting-approval'),
]

from .models import CityDistance


PRICE_PER_KM = 50  


def calculate_trip_price(origin, destination):
    route = CityDistance.objects.get(origin=origin, destination=destination)
    return route.distance_km * PRICE_PER_KM


def calculate_travel_time_minutes(origin, destination):
    route = CityDistance.objects.get(origin=origin, destination=destination)
    return route.base_time_minutes

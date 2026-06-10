from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import datetime

from accounts.models import DriverProfile, Vehicle
from cities.models import City, CityDistance
from trips.models import Trip
from wallets.services import WalletService
from .models import Ticket
from .services import TicketService, TicketPurchaseError

User = get_user_model()


class TicketServiceTests(TestCase):
    
    def setUp(self):
        # ایجاد شهرها
        self.city_tehran = City.objects.create(name="tehran")
        self.city_esfahan = City.objects.create(name="esfahan")
        
        # ایجاد فاصله
        CityDistance.objects.create(
            origin=self.city_tehran,
            destination=self.city_esfahan,
            distance_km=400,
            base_time_minutes=300
        )
        
        # ایجاد راننده
        driver_user = User.objects.create_user(
            username="driver1",
            phone_number="09120000001",
            password="pass",
            role=User.Role.DRIVER
        )
        self.driver_profile = DriverProfile.objects.create(
            user=driver_user,
            national_code="1234567890",
            license_number="L12345",
            is_approved=True
        )
        
        # ایجاد خودرو
        self.vehicle = Vehicle.objects.create(
            driver=self.driver_profile,
            plate_number="12-345-67",
            car_model="اسکانیا",
            capacity=40
        )
        
        # ایجاد خریدار
        self.user = User.objects.create_user(
            username="buyer1",
            phone_number="09120000002",
            password="pass",
            role=User.Role.USER
        )
        
        # شارژ کیف پول با 1,000,000 تومان
        WalletService.deposit(self.user, Decimal(1000000), " initial charge ")
        
        # ایجاد سفر معمولی (قیمت 200,000 تومان، تأیید شده)
        self.trip = Trip.objects.create(
            driver=self.driver_profile,
            vehicle=self.vehicle,
            origin=self.city_tehran,
            destination=self.city_esfahan,
            departure_time=timezone.now() + datetime.timedelta(days=1),
            capacity=40,
            price=200000,
            travel_time_minutes=300,
            status=Trip.Status.APPROVED
        )
    
    # تست خرید موفق
    def test_successful_ticket_purchase(self):
        initial_balance = self.user.wallet.balance
        ticket = TicketService.buy_ticket(
            user=self.user,
            trip=self.trip,
            seat_number=5
        )
        self.user.wallet.refresh_from_db()
        expected_balance = initial_balance - self.trip.price
        self.assertEqual(self.user.wallet.balance, expected_balance)
        self.assertIsNotNone(ticket.id)
        self.assertEqual(ticket.seat_number, 5)
        self.assertEqual(ticket.status, Ticket.Status.ACTIVE)
    
    # تست سفر تأیید نشده
    def test_trip_not_approved(self):
        self.trip.status = Trip.Status.PENDING
        self.trip.save()
        with self.assertRaises(TicketPurchaseError) as cm:
            TicketService.buy_ticket(user=self.user, trip=self.trip, seat_number=1)
        self.assertEqual(str(cm.exception), "Trip is not approved")
    
    #تست صندلی نامعتبر 
    def test_invalid_seat_number_negative(self):
        with self.assertRaises(TicketPurchaseError) as cm:
            TicketService.buy_ticket(user=self.user, trip=self.trip, seat_number=0)
        self.assertEqual(str(cm.exception), "Invalid seat number")
    
    #تست صندلی نامعتبر
    def test_invalid_seat_number_exceeds_capacity(self):
        with self.assertRaises(TicketPurchaseError) as cm:
            TicketService.buy_ticket(user=self.user, trip=self.trip, seat_number=100)
        self.assertEqual(str(cm.exception), "Invalid seat number")
    
    # تست صندلی تکراری
    def test_seat_already_reserved(self):
        TicketService.buy_ticket(user=self.user, trip=self.trip, seat_number=10)
        with self.assertRaises(TicketPurchaseError) as cm:
            TicketService.buy_ticket(user=self.user, trip=self.trip, seat_number=10)
        self.assertEqual(str(cm.exception), "Seat already reserved")
    
    # تست پر شدن ظرفیت
    def test_trip_full(self):
        # شارژ زیاد برای پر کردن کل ظرفیت
        WalletService.deposit(self.user, Decimal(10000000), "test balance")

        for seat in range(1, self.trip.capacity + 1):
            TicketService.buy_ticket(
                user=self.user,
                trip=self.trip,
                seat_number=seat
            )

        with self.assertRaises(TicketPurchaseError) as cm:
            TicketService.buy_ticket(
                user=self.user,
                trip=self.trip,
                seat_number=1
            )

        self.assertEqual(str(cm.exception), "Trip is full")

    def test_insufficient_balance(self):
        # موجودی را کم کن
        self.user.wallet.balance = Decimal(100000)
        self.user.wallet.save()
        with self.assertRaises(TicketPurchaseError) as cm:
            TicketService.buy_ticket(user=self.user, trip=self.trip, seat_number=20)
        self.assertEqual(str(cm.exception), "Insufficient balance")
    
        #تست سفر با قیمت صفر 
    def test_zero_price_trip(self):
        zero_trip = Trip.objects.create(
            driver=self.driver_profile,
            vehicle=self.vehicle,
            origin=self.city_tehran,
            destination=self.city_esfahan,
            departure_time=timezone.now() + datetime.timedelta(days=1),
            capacity=40,
            price= Decimal('0'),
            travel_time_minutes=300,
            status=Trip.Status.APPROVED
        )

        initial_balance = self.user.wallet.balance
        print(f"zero_trip.price = {zero_trip.price}, type = {type(zero_trip.price)}")
        ticket = TicketService.buy_ticket(user=self.user, trip=zero_trip, seat_number=1)
        self.user.wallet.refresh_from_db()
        # موجودی نباید تغییر کند
        self.assertEqual(self.user.wallet.balance, initial_balance)
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.seat_number, 1)
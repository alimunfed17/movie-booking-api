from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Movie, Show, Booking
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.tokens import RefreshToken

class BookingTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser",
            email="user@test.com",
            password="pass1234"
        )

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        self.movie = Movie.objects.create(title="Inception", duration_minutes=120)
        self.show = Show.objects.create(
            movie=self.movie,
            screen_name="Screen 1",
            date_time=timezone.now() + timedelta(days=1),
            total_seats=98,
        )

        self.book_url = reverse("booking", kwargs={"show_id": self.show.id})
        self.cancel_url = reverse("cancel", kwargs={"show_id": self.show.id})
        self.my_bookings_url = reverse("my-bookings")

    def test_successful_booking(self):
        """User can successfully book a seat"""
        data = {"seat_number": 5}
        response = self.client.post(self.book_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().seat_number, 5)

    def test_double_booking_not_allowed(self):
        """Seat cannot be booked twice for the same show"""
        Booking.objects.create(user=self.user, show=self.show, seat_number=10)
        data = {"seat_number": 10}
        response = self.client.post(self.book_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Seat already booked", response.data["detail"])

    def test_booking_nonexistent_show(self):
        """Trying to book a show that doesn't exist should fail"""
        fake_url = reverse("booking", kwargs={"show_id": 998})
        response = self.client.post(fake_url, {"seat_number": 9})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cancel_booking(self):
        """User can cancel a booking"""
        booking = Booking.objects.create(user=self.user, show=self.show, seat_number=8, status="booked")
        response = self.client.post(self.cancel_url, {"seat_number": 8})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        booking.refresh_from_db()
        self.assertEqual(booking.status, "cancelled")

    def test_cancel_nonexistent_booking(self):
        """Cancelling a non-existent booking return 404"""
        response = self.client.post(self.cancel_url, {"seat_number": 98})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_user_booking(self):
        """User can view their bookings"""
        Booking.objects.create(user=self.user, show=self.show, seat_number=7)
        response = self.client.get(self.my_bookings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["seat_number"], 7)
    
    def test_overbooking_prevention(self):
        """User cannot book a seat number greater than total seats"""
        data = {"seat_number": 150}
        response = self.client.post(self.book_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid seat number", response.data.get("detail", ""))

    def test_unauthorized_cancel(self):
        """A user cannot cancel another user's booking"""
        other_user = User.objects.create_user(username="otheruser", password="pass1234")
        booking = Booking.objects.create(user=other_user, show=self.show, seat_number=9, status="booked")
        response = self.client.post(self.cancel_url, {"seat_number": 9})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


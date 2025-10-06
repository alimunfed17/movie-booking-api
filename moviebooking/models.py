from django.db import models
from django.conf import settings

class Movie(models.Model):
    title = models.CharField(max_length=255)
    duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return self.title
    
class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="shows")
    screen_name = models.CharField(max_length=50)
    date_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.movie.title} - {self.screen_name} - {self.date_time}"
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="booking")
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="booking")
    seat_number = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='booked')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('show', 'seat_number')

    def __str__(self):
        return f"{self.user.username} - {self.show} - Seat {self.seat_number} ({self.status})"
    
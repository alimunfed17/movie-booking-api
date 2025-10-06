from django.contrib import admin
from .models import *

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'duration_minutes')

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'screen_name', 'date_time', 'total_seats')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'show', 'seat_number', 'status', 'created_at')
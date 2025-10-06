from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializers import *

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *data, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
class MoviesView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

class ShowsView(generics.ListAPIView):
    serializer_class = ShowSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        movie_id = self.kwargs.get("movie_id")
        movie = Movie.objects.get(id=movie_id)
        return movie.shows.all()
    
class BookShowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, show_id):
        seat_number = request.data.get("seat_number")

        if not seat_number:
            return Response({"detail": "Seat number is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            seat_number = int(seat_number)
        except ValueError:
            return Response({"detail": "Seat number must be an integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            show = Show.objects.get(pk=show_id)
        except Show.DoesNotExist:
            return Response({"detail": "Show not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if seat_number < 1 or seat_number > show.total_seats:
            return Response(
                {"detail": "Invalid seat number"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if Booking.objects.filter(show=show, seat_number=seat_number, status="booked").exists():
            return Response({"detail": "Seat already booked"}, status=status.HTTP_400_BAD_REQUEST)
        
        booking = Booking.objects.create(
            user=request.user,
            show=show,
            seat_number=seat_number,
            status="booked"
        )
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CancelShowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, show_id):
        seat_number = request.data.get("seat_number")
        if not seat_number:
            return Response({"detail": "Seat number is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            booking = Booking.objects.get(
                show_id=show_id,
                seat_number=seat_number,
                user=request.user,
                status="booked"
            )
        except Booking.DoesNotExist:
            return Response({'detail': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        
        booking.status = 'cancelled'
        booking.save()
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MyBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
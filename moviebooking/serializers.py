from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Movie, Show

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if user is None:
            raise serializers.ValidationError("Invalid Credentials")
        refresh = RefreshToken.for_user(user)
        return {
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
    
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["title", "duration_minutes"]

class ShowSerializer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source="movie.title")
    date_time = serializers.SerializerMethodField()

    class Meta:
        model = Show
        fields = ["screen_name", "date_time", "total_seats", "movie_title"]

    def get_date_time(self, obj):
        return obj.date_time.strftime("%Y-%m-%d %I:%M%p")
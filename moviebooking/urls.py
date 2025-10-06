from django.urls import path
from .views import *

urlpatterns = [
    # Auth
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),

    # Movie
    path("movies/", MoviesView.as_view(), name="movies")
]
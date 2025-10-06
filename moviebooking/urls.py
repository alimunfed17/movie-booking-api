from django.urls import path
from .views import *

urlpatterns = [
    # Auth
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),

    # Movies & Shows
    path("movies/", MoviesView.as_view(), name="movies"),
    path("movies/<int:movie_id>/shows/", ShowsView.as_view(), name="shows")
]
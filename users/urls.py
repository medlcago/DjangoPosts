from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import UserLogin, UserProfile

app_name = "users"

urlpatterns = [
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfile.as_view(), name="profile")
]

from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import UserLogin

app_name = "users"

urlpatterns = [
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout")
]

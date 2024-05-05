from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.users.views import UserLogin, UserProfile, ProfileUpdate

app_name = "users"

urlpatterns = [
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfile.as_view(), name="profile"),
    path("update-profile-photo/", csrf_exempt(ProfileUpdate.as_view()), name="update-profile-photo")
]

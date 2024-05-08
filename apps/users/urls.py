from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.users.views import (
    UserLoginView,
    UserProfileView,
    UpdateProfilePhotoView,
    UpdateProfileStatusView,
    UserRegistrationView
)

app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("update-profile-photo/", csrf_exempt(UpdateProfilePhotoView.as_view()), name="update-profile-photo"),
    path("update-profile-status/", csrf_exempt(UpdateProfileStatusView.as_view()), name="update-profile-status")
]

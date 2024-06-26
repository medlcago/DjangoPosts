import json

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView

from apps.users.forms import (
    UserLoginForm,
    UpdateProfilePhotoForm,
    UserRegistrationForm
)
from apps.users.services import user_service


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("users:profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Registration"
        return context

    def form_valid(self, form):
        user = form.save(commit=True)
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        remember_me = self.request.POST.get("remember-me", None)
        if remember_me is None:
            self.request.session.set_expiry(0)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        return context

    def get_success_url(self):
        return reverse_lazy("posts:posts")


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.request.user.username
        context["profile_page"] = True
        context["user"] = self.request.user
        context["posts"] = self.request.user.posts.all()[:10]
        context["update_profile_photo_form"] = UpdateProfilePhotoForm(instance=self.request.user.profile)
        return context


class UpdateProfilePhotoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return user_service.update_photo(
            profile=self.request.user.profile,
            files=self.request.FILES,
            request=request
        )


class UpdateProfileStatusView(LoginRequiredMixin, View):
    def patch(self, request, *args, **kwargs):
        data = json.loads(self.request.body)
        status = data.get("status")
        return user_service.update_status(
            profile=request.user.profile,
            status=status
        )

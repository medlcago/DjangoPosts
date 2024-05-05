from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from users.forms import UserLoginForm


class UserLogin(LoginView):
    authentication_form = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Login"
        return data

    def get_success_url(self):
        return reverse_lazy("posts:posts")


class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.request.user.username
        context["profile_page"] = True
        context["user"] = self.request.user
        context["posts"] = self.request.user.posts.all()[:10]
        return context

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

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

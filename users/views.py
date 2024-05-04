from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class UserLogin(LoginView):
    template_name = 'users/registration.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Login"
        return data

    def get_success_url(self):
        return reverse_lazy("posts:posts")

import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView

from apps.users.forms import UserLoginForm, UpdateProfilePhotoForm


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True

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


class UpdateProfilePhotoView(View):
    def post(self, request, *args, **kwargs):
        if request.FILES:
            profile = request.user.profile
            profile.avatar = request.FILES["file"]
            form = UpdateProfilePhotoForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return JsonResponse(data={
                    "message": "Photo updated success"
                },
                    status=200,
                    safe=False
                )
        return JsonResponse(data={
            "message": "Bad request"
        },
            status=400,
            safe=False
        )


class UpdateProfileStatusView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        status = data.get("status", None)
        if status is not None:
            profile = request.user.profile
            profile.status = status
            profile.save()
            return JsonResponse(data={
                "message": "Status updated success"
            },
                status=200
            )
        return JsonResponse(data={
            "message": "Bad request"
        },
            status=400
        )

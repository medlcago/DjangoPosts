from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class PostsView(LoginRequiredMixin, TemplateView):
    template_name = "posts/posts.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Posts"
        return data

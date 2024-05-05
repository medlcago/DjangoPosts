from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

from apps.posts.models import Post


class PostListView(LoginRequiredMixin, ListView):
    queryset = Post.published.select_related("author")
    context_object_name = "posts"
    template_name = "posts/post-list.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Posts"
        data["main_page"] = True
        data["user"] = self.request.user
        return data


class PostDetailView(LoginRequiredMixin, DetailView):
    queryset = Post.published.select_related("author")
    context_object_name = "post"
    template_name = "posts/post-detail.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["title"] = "Post"
        data["user"] = self.request.user
        return data

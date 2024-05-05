from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView

from apps.posts.forms import CreatePostForm
from apps.posts.models import Post


class PostListView(LoginRequiredMixin, ListView):
    queryset = Post.published.select_related("author").order_by("id")
    context_object_name = "posts"
    template_name = "posts/post-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Posts"
        context["main_page"] = True
        context["user"] = self.request.user
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    queryset = Post.published.select_related("author")
    context_object_name = "post"
    template_name = "posts/post-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Post"
        context["user"] = self.request.user
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = "posts/create-post.html"
    context_object_name = "form"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create post"
        context["user"] = self.request.user
        context["create_post_page"] = True
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return redirect(post.get_absolute_url())

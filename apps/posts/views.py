import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from apps.posts.forms import CreatePostForm
from apps.posts.models import Post
from apps.posts.services import post_service


class PostListView(LoginRequiredMixin, ListView):
    queryset = Post.objects.select_related("author").order_by("-created_at")
    context_object_name = "posts"
    template_name = "posts/post-list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Posts"
        context["main_page"] = True
        context["user"] = self.request.user
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    queryset = Post.objects.select_related("author")
    context_object_name = "post"
    template_name = "posts/post-detail.html"

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        post = self.object
        if not post.is_published and request.user.id != post.author.id:
            raise Http404
        return response

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


class UpdatePostView(LoginRequiredMixin, View):
    def post(self, request):
        data = json.loads(self.request.body)
        return post_service.update_post(
            user_id=request.user.id,
            **data
        )


class DeletePostView(LoginRequiredMixin, View):
    def delete(self, request):
        data = json.loads(self.request.body)
        pk = data.get("postId")
        return post_service.delete_post(
            user_id=request.user.id,
            pk=pk
        )

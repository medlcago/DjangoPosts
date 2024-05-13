import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from apps.posts.forms import CreatePostForm
from apps.posts.models import Post


class PostListView(LoginRequiredMixin, ListView):
    queryset = Post.objects.select_related("author").order_by("id")
    context_object_name = "posts"
    template_name = "posts/post-list.html"

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
        pk = data.get("postId")
        title = data.get("postTitle")
        description = data.get("postDescription")
        status = data.get("postStatus")

        if not all([pk, title, description, status]):
            return JsonResponse(data={
                "message": "Bad request"
            },
                status=400
            )

        post = get_object_or_404(Post, pk=pk)

        if self.request.user.id != post.author.id:
            return JsonResponse(data={
                "message": "Access denied"
            },
                status=403
            )

        post.title = title
        post.description = description
        post.is_published = status

        try:
            post.full_clean()
        except ValidationError as ex:
            error_dict = ex.message_dict
            errors = {field: messages for field, messages in error_dict.items()}
            return JsonResponse(data={
                "message": "Bad request",
                "errors": errors
            },
                status=400
            )

        post.save()
        return JsonResponse(data={
            "message": "Post successfully updated"
        },
            status=200
        )

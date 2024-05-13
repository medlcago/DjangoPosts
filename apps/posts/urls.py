from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.posts.views import (
    PostListView,
    PostDetailView,
    CreatePostView,
    UpdatePostView
)

app_name = "posts"

urlpatterns = [
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("posts/create/", CreatePostView.as_view(), name="create-post"),
    path("update-post/", csrf_exempt(UpdatePostView.as_view()), name="update-post")
]

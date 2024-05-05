from django.urls import path

from apps.posts.views import PostListView, PostDetailView, CreatePostView

app_name = "posts"

urlpatterns = [
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("posts/create/", CreatePostView.as_view(), name="create-post")
]

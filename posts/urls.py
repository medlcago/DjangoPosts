from django.urls import path

from posts.views import PostsView

app_name = "posts"

urlpatterns = [
    path("posts/", PostsView.as_view(), name="posts"),
]

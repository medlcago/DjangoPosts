from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="posts", null=True, verbose_name="Автор")
    title = models.CharField(max_length=255, blank=False, null=False, verbose_name="Заголовок")
    description = models.TextField(blank=False, null=False, verbose_name="Содержание поста")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("posts:post-detail", args=[self.id])

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

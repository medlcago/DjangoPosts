from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

User = get_user_model()


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = (0, "Черновик")
        PUBLISHED = (1, "Опубликовано")

    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="posts", null=True, verbose_name="Автор")
    title = models.CharField(max_length=255, blank=False, null=False, verbose_name="Заголовок")
    description = models.TextField(blank=False, null=False, verbose_name="Содержание поста")
    is_published: bool = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                             default=Status.DRAFT, verbose_name="Статус", blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("posts:post-detail", args=[self.id])

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

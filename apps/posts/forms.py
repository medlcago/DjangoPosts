from django import forms

from apps.posts.models import Post


class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_published"].initial = True

    class Meta:
        model = Post
        fields = ["title", "description", "is_published"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control form-widget",
                "required": True,
                "placeholder": "Заголовок поста"
            }),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control form-widget",
                    "required": True,
                    "placeholder": "Содержание поста"
                }
            ),
            "is_published": forms.Select(
                attrs={
                    "class": "form-control form-widget"
                })
        }

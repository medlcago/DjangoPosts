from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.update(
            {
                "password_mismatch": _("Пароли не совпадают")
            }
        )

        self.fields["username"].error_messages.update({
            "required": _("Поле является обязательным"),
            "unique": _("Имя пользователя уже используется")
        })

        self.fields["password1"].error_messages.update({
            "required": _("Поле является обязательным")
        })
        self.fields["password2"].error_messages.update({
            "required": _("Поле является обязательным")
        })

        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control form-widget",
                "placeholder":  _("Пароль")
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control form-widget",
                "placeholder": _("Подтвердите пароль")
            }
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["username"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control form-widget",
                "required": True,
                "placeholder": _("Имя пользователя")
            })
        }

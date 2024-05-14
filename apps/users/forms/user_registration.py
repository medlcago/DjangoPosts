import re

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

        self.fields["username"].widget.attrs.update({
            "minlength": 6,
            "maxlength": 16
        })

        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control form-widget",
                "placeholder": _("Пароль")
            }
        )
        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control form-widget",
                "placeholder": _("Подтвердите пароль")
            }
        )

    def clean_username(self):
        username = super().clean_username()
        if len(username) < 6:
            raise forms.ValidationError(_("Минимальная длина 6 символов"))
        if len(username) > 16:
            raise forms.ValidationError(_("Максимальная длина 16 символов"))
        if not re.fullmatch(r"^[A-Za-z][A-Za-z_.\\d]*[A-Za-z\\d]$", username):
            raise forms.ValidationError(_("Используйте только латинские символы и цифры"))
        return username

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

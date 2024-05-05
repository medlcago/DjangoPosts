from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from apps.users.models import Profile


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': _('Введите имя пользователя или email адрес'),
                'required': True,
                'minlength': 4,
                "maxlength": 32,
                "style": "border-radius: 10px;"
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': _('Введите пароль'),
                'required': True,
                'minlength': 6,
                'maxlength': 32,
                "style": "border-radius: 10px;"
            }
        )

        self.fields["username"].label = _("Имя пользователя/email адрес")
        self.fields["password"].label = _("Пароль")

    error_messages = {
        "invalid_login": _(
            "Неверный логин или пароль"
        ),
        "inactive": _(
            "Эта учетная запись неактивна"
        )
    }


class UpdateProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
        widgets = {
            "avatar": forms.FileInput(attrs={'id': 'formFile', 'accept': '.jpg,.jpeg,.png'})
        }

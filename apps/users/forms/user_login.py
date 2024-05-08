from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.update(
            {
                "invalid_login": _(
                    "Неверный логин или пароль"
                ),
                "inactive": _(
                    "Эта учетная запись неактивна"
                )
            })

        self.fields["username"].widget.attrs.update(
            {
                'class': 'form-control form-widget',
                'placeholder': _('Введите имя пользователя или email адрес'),
                'required': True,
                'minlength': 4,
                "maxlength": 32
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                'class': 'form-control form-widget',
                'placeholder': _('Введите пароль'),
                'required': True,
                'minlength': 6,
                'maxlength': 32
            }
        )

        self.fields["username"].label = _("Имя пользователя/email адрес")
        self.fields["password"].label = _("Пароль")

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session

from .models import Profile

User = get_user_model()
admin.site.unregister(User)


class ProfileInline(admin.StackedInline):
    model = Profile
    show_change_link = True


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ("session_key", "decoded_session_data", "expire_date")
    readonly_fields = ("session_key", "session_data", "decoded_session_data", "expire_date")
    ordering = ("-expire_date",)

    @staticmethod
    def decoded_session_data(obj):
        return obj.get_decoded()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    save_on_top = True
    readonly_fields = ("user",)
    list_select_related = ("user",)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "full_name", "is_staff", "last_login", "date_joined")
    inlines = [ProfileInline]

    @admin.display(description="Полное имя")
    def full_name(self, obj):
        return obj.first_name + " " + obj.last_name

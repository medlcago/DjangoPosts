from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Profile

User = get_user_model()
admin.site.unregister(User)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    save_on_top = True
    list_select_related = ("user", )


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "full_name", "is_staff", "last_login", "date_joined")

    @admin.display(description="Полное имя")
    def full_name(self, obj):
        return obj.first_name + " " + obj.last_name

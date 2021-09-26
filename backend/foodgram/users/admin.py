from django.contrib import admin

from .models import MyUser
from .profile import ProfileUser


class MyUserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "role")
    list_filter = ("username", "email")
    empty_value_display = "-пусто-"
    fields = ("first_name", "last_name", "email", "username", "password", "role")


class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ("user", )


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(ProfileUser, ProfileUserAdmin)

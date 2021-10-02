from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import MyUser
from .profile import ProfileUser

User = get_user_model()


class MyUserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "is_active")
    list_filter = ("username", "email")
    empty_value_display = "-пусто-"
    fields = (
        "first_name", "last_name", "email",
        "username", "password", "is_active",
    )

    def save_model(self, request, obj, form, change):
        orig_obj = User.objects.get(pk=obj.pk)
        if obj.password != orig_obj.password:
            obj.set_password(obj.password)
        obj.save()


class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ("user", )


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(ProfileUser, ProfileUserAdmin)

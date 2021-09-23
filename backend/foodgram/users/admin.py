from django.contrib import admin

from .models import MyUser


class MyUserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "role")
    search_fields = ("username",)
    empty_value_display = "-пусто-"
    fields = ("first_name", "last_name", "email", "username", "password", "role")


admin.site.register(MyUser, MyUserAdmin)

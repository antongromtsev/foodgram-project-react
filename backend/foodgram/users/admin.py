from django.contrib import admin

from .models import MyUser

class MyUserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "role")
    search_fields = ("username",)
    empty_value_display = "-пусто-"


admin.site.register(MyUser, MyUserAdmin)
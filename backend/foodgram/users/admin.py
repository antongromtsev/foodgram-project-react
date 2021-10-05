from django.contrib import admin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import MyUser
from .profile import Favourites, Shopping_cart, Subscription

User = get_user_model()


# class SubscriptionInline (admin.TabularInline):
#     model = Subscription
#     extra = 1

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'
    fields = (
        'first_name', 'last_name', 'email',
        'username', 'password', 'is_active',
    )

    def save_model(self, request, obj, form, change):
        orig_obj = get_object_or_404(User, pk=obj.pk)
        if obj.password != orig_obj.password:
            obj.set_password(obj.password)
        obj.save()


# # class FavouritesAdmin(admin.ModelAdmin):
# #     #list_display = ('user__usermane', 'recipe__name')
# #     inlines = (IngredientValueInline,)

# # class Shopping_cartAdmin(admin.ModelAdmin):
# #     #list_display = ('follower__username', 'followed__username')
# #     inlines = (IngredientValueInline,)

# class SubscriptionAdmin(admin.ModelAdmin):
#     #list_display = ('user__username', 'recipe__name')
#     inlines = (SubscriptionInline,)

admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Favourites,)
admin.site.register(Shopping_cart,)
admin.site.register(Subscription,)

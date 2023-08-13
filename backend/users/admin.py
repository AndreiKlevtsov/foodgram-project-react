from django.contrib import admin

from .models import CustomUser, Subscription

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'password',
        'email',
        'first_name',
        'last_name'
    )
    search_fields = ('email', 'first_name',)
    list_filter = ('email', 'first_name',)
    empty_value_display = '-пусто-'

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'author',
    )
    search_fields = ('author',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'

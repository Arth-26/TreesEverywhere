from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .admin_actions import *
from .models import *

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'date_joined', 'profile_about')
    list_display_links = ('username', 'email')
    search_fields = ('username', 'email')
    list_per_page = 10

    fieldsets = (
        (None, {'fields': ('username', 'email', 'accounts')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'accounts'),
        }),
    )

class Accounts(admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'active')
    list_display_links = ('name',)
    search_fields = ('name', 'creation_date')
    list_per_page = 10
    actions = [activate_accounts, deactivate_accounts]

class Profiles(admin.ModelAdmin):
    list_display = ('user', 'about', 'date_joined')
    list_display_links = ('user',)
    search_fields = ('user', 'date_joined')
    list_per_page = 10


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Account, Accounts)
admin.site.register(Profile, Profiles)
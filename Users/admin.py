from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')
    list_display_links = ('username', 'email')
    search_fields = ('username', 'email')
    list_per_page = 10

    fieldsets = (
        (None, {'fields': ('username', 'email', 'date_joined', 'accounts')}),
    )

class Accounts(admin.ModelAdmin):
    list_display = ('name', 'creation_date', 'active')
    list_display_links = ('name',)
    search_fields = ('name', 'creation_date',)
    list_per_page = 10


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Account, Accounts)
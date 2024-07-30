from django.contrib import admin

@admin.action(description='Activate selected accounts')
def activate_accounts(modeladmin, request, queryset):
    queryset.update(active=True)

@admin.action(description='Deactivate selected accounts')
def deactivate_accounts(modeladmin, request, queryset):
    queryset.update(active=False)

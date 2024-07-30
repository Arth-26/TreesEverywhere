from django.contrib import admin
from .models import *


# Class to show planted trees in the tree admin interface
class PlantedTreeInline(admin.TabularInline):
    model = PlantedTree
    extra = 0
    fields = ('get_user', 'get_account', 'planted_at', 'location')
    readonly_fields = ('get_user', 'get_account', 'planted_at', 'location')
    can_delete = False

    # The functions below are used to customize the description of attributes in the administrative interface
    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User'

    def get_account(self, obj):
        return obj.user.email
    get_account.short_description = 'Account'


class Trees(admin.ModelAdmin):
    list_display = ('name', 'scientific_name', 'count_planted_trees')
    list_display_links = ('name', 'scientific_name')
    search_fields = ('name', 'scientific_name')
    list_per_page = 10
    inlines = [PlantedTreeInline]

class PlantedTrees(admin.ModelAdmin):
    list_display = ('get_user', 'get_account', 'planted_tree', 'age', 'planted_at', 'location')
    list_display_links = ('get_user', 'get_account', 'planted_tree')
    search_fields = ('get_user', 'get_account', 'planted_tree', 'planted_at')
    list_per_page = 10

    
    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User'

    def get_account(self, obj):
        return obj.user.email
    get_account.short_description = 'Account'

admin.site.register(Plant, Trees)
admin.site.register(PlantedTree, PlantedTrees)

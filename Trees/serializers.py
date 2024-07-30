from rest_framework import serializers
from .models import PlantedTree

class PlantedTreeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    account = serializers.SerializerMethodField()
    tree = serializers.SerializerMethodField()
    location = serializers.CharField()

    class Meta:
        model = PlantedTree
        fields = ['id', 'tree', 'user', 'account', 'planted_at', 'age', 'location']

    # Funnctions to show important data from model-related tables
    def get_user(self, obj):
        return obj.user.username

    def get_account(self, obj):
        return obj.account.name

    def get_tree(self, obj):
        return obj.tree.name
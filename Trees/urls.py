from django.urls import path
from .views import *

app_name = 'trees'

urlpatterns = [
    path('api/user/planted-trees/', UserPlantedTreesView.as_view(), name='user-planted-trees'),
    path('green_area/<int:account_id>', green_area, name='green_area'),
    path('garden/user/<int:user_id>/account/<int:account_id>', TreeList.as_view(), name='garden'),
    path('account_garden/<int:account_id>', AccountTreeList.as_view(), name='account_garden'),
    path('tree/<int:pk>/user/<int:user_id>/account/<int:account_id>', PlantedTreeDetailView.as_view(), name='tree_detail'),
    path('plant_tree/user/<int:user_id>/account/<int:account_id>', PlantTreeView.as_view(), name='plant_tree'),
    path('plant_more_tree/user/<int:user_id>/account/<int:account_id>', PlantMoreTreeView.as_view(), name='plant_trees'),
]
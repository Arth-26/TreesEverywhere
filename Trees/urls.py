from django.urls import path
from .views import *

app_name = 'trees'

urlpatterns = [
    path('api/user/planted-trees/', UserPlantedTreesView.as_view(), name='user-planted-trees'),
    path('green_area/<int:account_id>', green_area, name='green_area'),
    path('garden/user/<int:user_id>/account/<int:account_id>', TreeList.as_view(), name='garden'),
    path('tree/<int:pk>/user/<int:user_id>/account/<int:account_id>', PlantedTreeDetailView.as_view(), name='tree_detail')
]
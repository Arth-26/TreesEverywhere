from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('account_hub/<int:account_id>', account_hub, name='hub'),
    path('account/<int:account_id>/friends', UsersAccount.as_view(), name='friends'),
    path('logout/', logout_view, name='logout'),
]


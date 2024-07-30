from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PlantedTree
from .serializers import PlantedTreeSerializer
from Users.models import CustomUser, Account
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import *

@login_required
def green_area(request, account_id):
    account = Account.objects.get(pk=account_id)
    user = request.user
    context= {
        'account': account,
        'user': user
    }
    
    return render(request, 'green_area.html', context)

class TreeList(LoginRequiredMixin, ListView):
    model = PlantedTree
    template_name = 'garden.html'
    context_object_name = 'trees'

    def get_queryset(self, **kwargs):
        account_id = self.kwargs.get('account_id')
        user = self.request.user
        
        return PlantedTree.objects.filter(account__id=account_id, user=user)

    def get_context_data(self, **kwargs):
        account = Account.objects.get(id=self.kwargs.get('account_id'))
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['account'] = account
        return context

class PlantedTreeDetailView(DetailView):
    model = PlantedTree
    template_name = 'planted_tree_detail.html'
    context_object_name = 'tree'

    def get_context_data(self, **kwargs):
        account = Account.objects.get(id=self.kwargs.get('account_id'))
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['account'] = account
        return context








class UserPlantedTreesView(APIView):
    # Just autenthicated users can use this request method
    permission_classes = [IsAuthenticated]

    # Function
    def get(self, request):
        user = request.user
        planted_trees = PlantedTree.objects.filter(user=user)
        serializer = PlantedTreeSerializer(planted_trees, many=True)
        return Response(serializer.data)
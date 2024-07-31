from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PlantedTree
from .forms import *
from .serializers import PlantedTreeSerializer
from Users.models import CustomUser, Account
from django.views.generic import ListView, DetailView, FormView
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

class AccountTreeList(LoginRequiredMixin, ListView):
    model = PlantedTree
    template_name = 'account_garden.html'
    context_object_name = 'trees'

    def get_queryset(self, **kwargs):
        account_id = self.kwargs.get('account_id')
        
        return PlantedTree.objects.filter(account__id=account_id)
    
    def get_context_data(self, **kwargs):
        account = Account.objects.get(id=self.kwargs.get('account_id'))
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['account'] = account
        return context

class PlantedTreeDetailView(LoginRequiredMixin, DetailView):
    model = PlantedTree
    template_name = 'planted_tree_detail.html'
    context_object_name = 'tree'

    def get_context_data(self, **kwargs):
        account = Account.objects.get(id=self.kwargs.get('account_id'))
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['account'] = account
        return context
    
    def dispatch(self, request, *args, **kwargs):
        planted_tree = self.get_object()

        if planted_tree.user != request.user:
            raise PermissionDenied  

        return super().dispatch(request, *args, **kwargs)

class PlantTreeView(LoginRequiredMixin, FormView):
    form_class = PlantTreeForm
    template_name = 'plant_tree.html'

    def form_valid(self, form, **kwargs):
        account = Account.objects.get(pk=self.kwargs.get('account_id'))
        tree = form.cleaned_data['tree']
        latitude = form.cleaned_data['latitude']
        longitude = form.cleaned_data['longitude']
        self.request.user.plant_tree(tree, (latitude, longitude), account)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        account = Account.objects.get(id=self.kwargs.get('account_id'))
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['account'] = account
        return context
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('trees:green_area', kwargs={'account_id': self.kwargs.get('account_id')})

class PlantMoreTreeView(LoginRequiredMixin, FormView):
    form_class = PlantMoreTreeForm
    template_name = 'plant_more_tree.html'

    def form_valid(self, form, **kwargs):
        account = Account.objects.get(pk=self.kwargs.get('account_id'))
        trees = form.cleaned_data['trees']

        trees_with_locations = []
        # Get all selected trees
        for index, tree in enumerate(trees):
            # Get the latitude and longitude field for each tree 
            latitude = self.request.POST.get(f'latitude_{tree.id}')
            longitude = self.request.POST.get(f'longitude_{tree.id}')

            trees_with_locations.append((tree, latitude, longitude))


        # Call de function plant_trees
        self.request.user.plant_trees(trees_with_locations, account)

        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        account = Account.objects.get(id=self.kwargs.get('account_id'))
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['account'] = account
        return context
    
    def get_success_url(self, **kwargs):
        return reverse_lazy('trees:green_area', kwargs={'account_id': self.kwargs.get('account_id')})


class UserPlantedTreesView(APIView):
    # Just autenthicated users can use this request method
    permission_classes = [IsAuthenticated]

    # Function
    def get(self, request):
        user = request.user
        planted_trees = PlantedTree.objects.filter(user=user)
        serializer = PlantedTreeSerializer(planted_trees, many=True)
        return Response(serializer.data)
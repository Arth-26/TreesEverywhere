from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import logout as auth_logout

def logout_view(request):
    auth_logout(request)
    return redirect('login')

class CustomLoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')  # Redireciona para a página 'home' após login bem-sucedido

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return super().form_valid(form)

class HomeView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'home.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        user = self.request.user
        return user.accounts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

@login_required
def account_hub(request, account_id):
    account = Account.objects.get(pk=account_id)
    context = {
        'account': account
    }
    return render(request, 'account_hub.html', context)

class UsersAccount(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = 'users_account.html'
    context_object_name = 'users'

    def get_queryset(self, **kwargs):
        account_id = self.kwargs.get('account_id')
        
        return CustomUser.objects.filter(accounts__id=account_id)

    def get_context_data(self, **kwargs):
        account = Account.objects.get(id=self.kwargs.get('account_id'))
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['account'] = account
        return context



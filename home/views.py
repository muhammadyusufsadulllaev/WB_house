from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from .forms import *
from .models import *

import time
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views import View


# Create your views here.

class HouseListView(ListView):
    model = House
    template_name = 'index.html'

    def get_queryset(self):
        if len(self.request.GET.dict().items()) == 0:
            query = self.request.COOKIES.copy()
            if 'sessionid' in query:
                del query['sessionid']
            if 'csrftoken' in query:
                del query['csrftoken']
        else:
            query = self.request.GET.dict()
        
        return House.objects.filter(**query)
    
    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        for key, val in self.request.GET.dict().items():
            response.set_cookie(key=key, value=val)
        return response


class HouseCreateView(CreateView):
    model = House
    fields = '__all__'
    template_name = 'add-house.html'
    success_url = reverse_lazy('index')


class HouseDeleteView(DeleteView):
    model = House
    success_url = reverse_lazy('index')
    template_name = 'house_delete.html'


class HouseUpdateView(UpdateView):
    model = House
    template_name = 'house-view.html'
    fields = '__all__'
    success_url = reverse_lazy('index')


def login_view(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, template_name='login.html', context={'form': form})
    else:
        from django.contrib.auth import login, authenticate
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect(reverse_lazy('index'))
        return render(request, template_name='login.html', context={'form': form, 'error_msg': 'Please, type correct user name and password'})

def logout_request(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect(reverse_lazy("index"))

def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, template_name='register.html', context={'form': form})
    else:
        from django.contrib.auth import login, authenticate
        form = RegisterForm(data=request.POST)
        if form.is_valid():

            user = form.instance
            user.set_password(request.POST['password'])
            form.save()

            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user:
                login(request, user)
                return redirect(reverse_lazy('index'))
            return render(request, template_name='register.html', context={'form': form, 'error_msg': 'Please, type correct user name and password'})
        
        return render(request, template_name='register.html', context={'form': form})

# Create your views here.
def login_view(request):
    if request.method =='GET':
        form = LoginForm()
        return render(request, template_name='login.html',context={'form':form})
    else:
        from django.contrib.auth import login,authenticate
        user = authenticate(request, username = request.POST['username'],password = request.POST['password'])
        if user:
            login(request, user)
        else:
            form = LoginForm()
            return render(request, template_name='login.html',context={'form':form, 'error_msg': 'Please, type correct user name and password'})

def logout_request(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect(reverse_lazy("index"))

def register_view(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, template_name='register.html', context={'form': form})
    else:
        from django.contrib.auth import login, authenticate
        form = RegisterForm(data=request.POST)
        if form.is_valid():

            user = form.instance
            user.set_password(request.POST['password'])
            form.save()

            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user:
                login(request, user)
            return render(request, template_name='register.html', context={'form': form, 'error_msg': 'Please, type correct user name and password'})
        
        return render(request, template_name='register.html', context={'form': form})

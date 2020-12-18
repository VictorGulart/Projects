from django.core.checks import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone

# Sessions - logins, registrations, authentication, flash messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required # to see the page login is required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages


from .decorators import unauthenticated_user, allowed_users


from .models import Task
from .forms import TaskForm, CreateUserForm
import json
# Create your views here.

@login_required(login_url='todoapp:login')
@allowed_users(allowed_roles=['admin', 'users'])
def home_view( request, *args, **kwargs):

    context = {
        'tasks':Task.objects.filter(user=request.user)
    }
    return render( request, 'todoapp/home.html', context) 

@unauthenticated_user
def login_page( request ):
    context = {}
    if  request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('todoapp:home')
        else:
            messages.info(request, 'Username or Password is incorrect.')
    return render( request, 'todoapp/login.html', context)

@login_required(login_url='todoapp:login')
def logout_view( request ):
    logout(request)
    return redirect('todoapp:login')

@unauthenticated_user
def register_page( request ):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            username = username.capitalize()

            group = Group.objects.get(name='users')
            user.groups.add(group)

            messages.success( request, f'Account was created for {username}')
            return redirect('todoapp:login')

    context = {'form':form}
    return render( request, 'todoapp/register.html', context)

@login_required(login_url='todoapp:login')
def add_task( request, *args, **kwargs):
    ''' Creates a default task and returns the updated list '''
    if request.method == 'POST':
        task = Task() # Creates an empty task
        task.user = request.user
        task.save()
    return list_view( request )

@login_required(login_url='todoapp:login')
def list_view( request, *args, **kwargs):
    ''' Returns the list to update the main page '''
    tasks = Task.objects.filter(user=request.user)
    context = {
        'tasks':tasks
    }
    return render( request, 'todoapp/list.html', context)

@login_required(login_url='todoapp:login')
def edit_view(request, pk, *args, **kwargs):
    task = get_object_or_404( Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task) 
    if form.is_valid():
        form.save()
    context = {'form':form }
    return render(request, 'todoapp/edit_task.html', context)

@login_required(login_url='todoapp:login')
def get_modal_view( request, pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(instance=task) 
    context = {'form':form }
    return render(request, 'todoapp/task_form.html', context)

@login_required(login_url='todoapp:login')
def edit_modal_view( request, pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task) 
    if form.is_valid():
        form.save() 
    context = {'form':form }
    return HttpResponse('Success')


@login_required(login_url='todoapp:login')
def delete_view( request, pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        print('DELETED WITH SUCCESS')
        task.delete()
    return list_view( request ) 
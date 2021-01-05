import json
from django.core.checks import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone

# Sessions - logins, registrations, authentication, flash messages
from django.contrib.auth.decorators import login_required # to see the page login is required
from django.contrib import messages

# Todoapp imports
from .models import Task
from .forms import TaskForm

@login_required(login_url='account:login')
def home_view( request, *args, **kwargs):
    context = {
        'tasks':Task.objects.filter(user=request.user)
    }
    return render( request, 'todoapp/home.html', context) 

@login_required(login_url='account:login')
def add_task( request, *args, **kwargs):
    ''' Creates a default task and returns the updated list '''
    if request.method == 'POST':
        task = Task() # Creates an empty task
        task.user = request.user
        task.save()
    return list_view( request )

@login_required(login_url='account:login')
def list_view( request, *args, **kwargs):
    ''' Returns the list to update the main page '''
    tasks = Task.objects.filter(user=request.user)
    context = {
        'tasks':tasks
    }
    return render( request, 'todoapp/list.html', context)

@login_required(login_url='account:login')
def edit_view(request, pk, *args, **kwargs):
    task = get_object_or_404( Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task) 
    if form.is_valid():
        form.save()
    context = {'form':form, 'modal':False }
    return render(request, 'todoapp/edit_task.html', context)

@login_required(login_url='account:login')
def get_modal_view( request, pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(instance=task) 
    context = {'form':form, 'modal':True }
    return render(request, 'todoapp/task_form.html', context)

@login_required(login_url='account:login')
def edit_modal_view( request, pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task) 
    if form.is_valid():
        form.save() 
    context = {'form':form }
    return HttpResponse('Success')


@login_required(login_url='account:login')
def delete_view( request, pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        print('DELETED WITH SUCCESS')
        task.delete()
    return list_view( request ) 

@login_required(login_url='account:login')
def update_checkbox( request, pk ):
    # Negate the present value
    # use the message system to pass the message if failed to the top of the page
    if request.method == 'POST':
        task = Task.objects.get(pk=pk)
        task.checked = not task.checked
        task.save()
        return HttpResponse('Success')
    else:
        return HttpResponse('Failed')

@login_required(login_url='account:login')
def check_all_boxes_view( request ):
    if request.method == 'POST':
        tasks = Task.objects.filter(user = request.user)
        for task in tasks:
            if task.checked == False:
                task.checked = not task.checked
            else:
                continue
            task.save()
        return HttpResponse('Success')
        
    return HttpResponse('Failed')
    
@login_required(login_url='account:login')
def delete_all_checked_view( request ):
    if request.method == 'POST':
        tasks = Task.objects.filter(user = request.user)
        for task in tasks:
            if task.checked:
                task.delete()
        return HttpResponse('Success')
    return HttpResponse('Failed')

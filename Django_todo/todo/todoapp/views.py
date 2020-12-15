from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone
from .models import Task
from .forms import TaskForm, TaskRawForm
import json
# Create your views here.


def home_view( request, *args, **kwargs):

    context = {
        'tasks':Task.objects.all()
    }
    return render( request, 'todoapp/home.html', context) 

def add_task( request, *args, **kwargs):
    ''' Creates a default task and returns the updated list '''
    if request.method == 'POST':
        task = Task() # Creates an empty task
        task.save()
    print('CREATED NEW TASK')
    return list_view( request )

def list_view( request, *args, **kwargs):
    ''' Returns the list to update the main page '''
    tasks = Task.objects.all()
    context = {
        'tasks':tasks
    }
    return render( request, 'todoapp/list.html', context)

def edit_view(request, pk, *args, **kwargs):
    task = get_object_or_404( Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task) 
    if form.is_valid():
        form.save()
    context = {'form':form }
    return render(request, 'todoapp/edit_task.html', context)

def get_modal_view( request, pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(instance=task) 
    context = {'form':form }
    return render(request, 'todoapp/task_form.html', context)

def edit_modal_view( request, pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task) 
    if form.is_valid():
        form.save() 
    context = {'form':form }
    return HttpResponse('Success')


def delete_view( request, pk, *args, **kwargs):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        print('DELETED WITH SUCCESS')
        task.delete()
    return list_view( request ) 
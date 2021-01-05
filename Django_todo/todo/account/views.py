from django.shortcuts import render, get_object_or_404, redirect

# Django Authentication, Sessions, Messages
from django.contrib.auth.views import LoginView # for later implementations
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
 
# Account App Imports
from .forms import UserCreateForm
from .decorators import unauthenticated_user, allowed_users 

@unauthenticated_user
def login_view( request ):
    context = {}
    if  request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('todoapp:home')
        else:
            messages.info(request, 'Username or Password is incorrect.')
    return render( request, 'account/login.html', context)

@login_required(login_url='account:login')
def logout_view( request ):
    logout(request)
    return redirect('account:login')

@unauthenticated_user
def register_view( request ):
    form = UserCreateForm()
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()

            # group = Group.objects.get(name='users')
            # user.groups.add(group)

            messages.success( request, f'Account was created!')
            return redirect('account:login')

    context = {'form':form}
    return render( request, 'account/register.html', context)



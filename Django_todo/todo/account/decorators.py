from django.http import HttpResponse
from django.shortcuts import redirect


# stop the user to see the register and login pages
def unauthenticated_user(view):
    def wrapper_func(request, *args, **kwargs):
        # check if the a user has already loged on
        if request.user.is_authenticated:
            return redirect('todoapp:home')
        return view(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view):
        def wrapper_func(request, *args, **kwargs):
            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group not in allowed_roles:
                return HttpResponse('Not authorized to view the page')

            return view(request, *args, **kwargs)
        return wrapper_func
    return decorator

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # base class

# import forms to create the user creation view, update view and admin creation too
from .forms import UserAdminCreateForm, UserAdminUpdateForm
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # set forms to create and update admin user
    form = UserAdminUpdateForm
    add_form =  UserAdminCreateForm

    # Set fields to be use in displaying the User Model
    list_display    = ('email', 'admin', 'staff', 'active')
    list_filter     = ('admin', ) 
    fieldsets       = (
                (None,              {'fields': ('email', 'password')}), 
                ('Personal Info',   {'fields': () }), # no info at the moment
                ('Permissions',     {'fields': ( 'active', 'staff', 'admin',)}), 
    )

    add_fieldsets   = (
                (None, {'classes':('wide', ), 
                        'fields':('email', 'password1', 'password2')}),
    )

    search_fields   = ('email', ) # enable search on the view

    ordering        = ('email', ) 
    filter_horizontal = ()

# User = get_user_model()
# class UserAdmin(admin.ModelAdmin):
#     search_fields = ['email']
#     class Meta:
#         model = User
        

# Register your models here. This can also be done with class decorators
# admin.site.register(User, UserAdmin)

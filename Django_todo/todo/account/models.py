from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
    '''

    '''
    def create_user( self, email, password=None, is_active=True, is_staff=False, is_admin=False ):
        '''
            Create a user with the given email and password
            If there were other required field than it would be necessary
            to add them as args to the method and also to create_staffuser and 
            create_superuser
        '''
        if not email:
            raise ValueError('Users must have an email')
        if not password:
            raise ValueError('Users must have a password')
        user = self.model(
                email = self.normalize_email( email )
        )
        user.set_password( password ) # this will hash it, this is also how to change the password

        # Set permissions
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin

        user.save( using=self._db)
        return user

    def create_staffuser( self, email, password=None ):
        '''
            Create a staff user with the given email and password
        '''
        user = self.create_user(
                email,
                password = password,
                is_staff = True
        )
        return user

    def create_superuser( self, email, password=None ):
        '''
            Create a admin user with the given email and password
        '''
        user = self.create_user(
                email,
                password = password,
                is_staff = True,
                is_admin = True
        )
        return user


class User(AbstractBaseUser):
    '''
        Keep this model simple, if necessary to have a profile or to extend this model
        than just create a new profile app that will handle that 
        No need to set up password, it is built in
    
    '''
    email           = models.EmailField(
                            verbose_name='email address',
                            max_length=255,
                            unique=True
                            )
    username        = models.CharField(max_length=60)
    first_name      = models.CharField(max_length=30)
    last_name       = models.CharField(max_length=255)
    date_joined     = models.DateTimeField(default=timezone.now)
    active          = models.BooleanField(default=True)
    staff           = models.BooleanField(default=False)
    admin           = models.BooleanField(default=False) # this is the super user
    timestamp       = models.DateTimeField(auto_now_add=True)
    # confirm         = models.BooleanField(default=False) # confirm email
    # confirm_date    = models.DateTimeField(default=timezone.now) 

    USERNAME_FIELD = 'email'

    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = [] # will be called on 'py manage.py createsuperuser'

    objects = UserManager()

    @property
    def is_active( self ):
        ''' Is the user active '''
        return self.active
    
    @property
    def is_staff( self ):
        ''' Is the user staff '''
        return self.staff
    
    @property
    def is_admin( self ):
        ''' Is the user admin '''
        return self.admin
    
    def __str__( self ):
        return self.email

    def get_full_name( self ):
        return self.email 
    
    def get_short_name( self ):
        return self.email

    def has_perm( self, perm, obj=None ):
        ''' Does the user have a specific permission '''
        return self.is_admin
    
    def has_module_perms( self, app_label):
        ''' Does the user has permission to view the app `app_label` '''
        return True

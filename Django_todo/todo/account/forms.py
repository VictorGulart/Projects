from django.forms import ModelForm, CharField, EmailField, EmailInput, PasswordInput, ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

class UserCreateForm(ModelForm):
    '''
        A form to create an admin user, from the given
        email and password.
    '''
    # set some error messages dictionary to be easier to handle
    error_messages = {
        'password_mismatch': 'The two password fields didn\'t match.',
    }

    # set the fields
    email = EmailField(widget=EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    password1 = CharField(label='Password', widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'*****'}))
    password2 = CharField(label='Password Confirmation', widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'*****'}),
                                help_text='Enter the same password as above',
    )

    class Meta:
        model   = User
        fields  = ('email', )

    def clean_email( self ):
        email = self.cleaned_data.get( 'email' )
        qs = User.objects.filter( email=email )
        if qs.exists():
            raise ValidationError( 'Email is taken' )
        return email
    
    def clean_password2( self ):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError(
                        self.error_messages['password_mismatch']
            )
        return password2

    def save( self, commit=True ):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

   
class UserAdminCreateForm(ModelForm):
    '''
        A form to create an admin user, from the given
        email and password.
    '''
    # set some error messages dictionary to be easier to handle
    error_messages = {
        'password_mismatch': 'The two password fields didn\'t match.',
    }

    # set the fields
    password1 = CharField(label='Password', widget=PasswordInput)
    password2 = CharField(label='Password Confirmation', widget=PasswordInput,
                                help_text='Enter the same password as above',
    )

    class Meta:
        model   = User
        fields  = ('email', )
    
    def clean_password2( self ):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError(
                        self.error_messages['password_mismatch'],
            )
        return password2
    
    def save( self, commit=True ):
        user = super(UserAdminCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserAdminUpdateForm(ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ( 'email', 'password', 'active', 'staff', 'admin' )

    def clean_password( self ):
        return self.initial['password']
    

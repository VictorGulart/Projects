# Django import
from django.test import TestCase
from django.contrib.auth.models import User

# My Apps import
from .models import Task

# Create your tests here.

class TaskTestCase(TestCase):
    def setUp( self ):
        # print('Creating User')
        User.objects.create_user('naruto', 'naruto@gmail.com', 'learncode20') # creates an user to use for testing
    
    def test_empty_task( self ):
        ''' Creates an empty task just using default values with the user '''
        user = User.objects.get(username='naruto')
        task = Task.objects.create(user=user)
        task.save()
    
    def test_giving_title_task( self ):
        ''' Creates a task setting a title '''
        user = User.objects.get(username='naruto')
        task = Task.objects.create(user=user, title='Title Test')
        task.save()
 
    def test_giving_message_task( self ):
        ''' Creates a task setting a message '''
        user = User.objects.get(username='naruto')
        task = Task.objects.create(user=user, message='Message Test')
        task.save()
    
    def test_changing_message( self ):
        ''' Creates a task editting a message '''
        user = User.objects.get(username='naruto')
        task = Task.objects.create(user=user, message='Message Test')
        task.save()

        # Change Message
        task.message = 'New Message Test'
        task.save()
    
    def test_changing_message_short( self ):
        ''' Editting a message but is too short '''
        user = User.objects.get(username='naruto')
        task = Task.objects.create(user=user, message='Message Test')
        task.save()

        # Change Message
        task.message = 'New'
        task.save()
 
 
 



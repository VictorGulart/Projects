from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from todoapp.models import Task

# automated 
# new / blank db

User = get_user_model()

class TaskTestCase(APITestCase):

    def setUp(self):
        ## crate somethings that are related to the testing 
        # print('Creating User on API')
        user = User.objects.create(username='testUser', email='test@test.com') 
        user.set_password("somepassword")
        user.save()
        tasks = Task.objects.create(
            user=user, 
            title='Testing', 
            message='This is content', 
            checked=False
        )
    
    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
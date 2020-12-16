from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.TextField()
    email = models.EmailField(blank=True, null=True)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(default='Add Title', max_length=200)
    message = models.TextField(default='Add Notes')
    pub_date = models.DateTimeField(default=timezone.now)
    checked = models.BooleanField(default=False)

    def __str__( self ):
        return str( self.title )
    
    @property
    def owner( self ):
        return self.user
from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.


# class User(models.Model):
#     username = models.TextField()

class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(default='Add Title', max_length=200)
    message = models.TextField(default='Add Notes')
    pub_date = models.DateTimeField(default=timezone.now)
    checked = models.BooleanField(default=False)

    def __str__( self ):
        return str( self.user )
    
    @property
    def owner( self ):
        return self.user
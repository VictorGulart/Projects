from django.conf import settings
from django.db import models
from django.utils import timezone
from django.conf import settings
# from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(default='Add Title', max_length=200)
    message = models.TextField(default='Add Notes')
    pub_date = models.DateTimeField(default=timezone.now)
    checked = models.BooleanField(default=False)

    def __str__( self ):
        msg = f'\'{self.title}\' user: {self.user.username}'
        return str( msg )
    
    @property
    def owner( self ):
        return self.user
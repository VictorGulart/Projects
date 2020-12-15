import datetime

from django.db import models
from django.utils import timezone

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__( self ):
        return self.question_text

    def was_pub_recently( self ):
        ''' Adding a check to see if it was published within 24hs '''
        now  = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_pub_recently.admin_order_field = 'pub_date'
    was_pub_recently.admin_boolean = True
    was_pub_recently.short_description = 'Published recently?'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # defining a relationship
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__( self ):
        return self.choice_text

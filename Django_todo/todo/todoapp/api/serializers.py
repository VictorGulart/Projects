from rest_framework import routers, serializers, viewsets
from django.utils import timezone
from todoapp.models import Task

class TaskSerializer(serializers.ModelSerializer): # similar to forms.ModelForm
    message = serializers.CharField(min_length=2, max_length=200) # adding some extra validation with 

    class Meta:
        model = Task
        fields = [
            'pk',
            'title',
            'message',
            'checked'
        ]

        ## read_only = [
        ##     'pk', 'title'
        ## ]

    def to_representation( self, instance ):
        ''' Adding info to the serialization '''
        data = super().to_representation( instance ) 
        data['current_date'] = timezone.now() # no use for it just to show its possible to return more info
        return data

    def validate_title(self, value):
        ''' Checks whether the title is already in use '''
        ts = Task.objects.filter(title__iexact=value) # includes the current instance so it is always wrong
        if self.instance:
            ts = ts.exclude(pk=self.instance.pk)
        if ts.exists():
            raise serializers.ValidationError("This title has been taken")
        return value
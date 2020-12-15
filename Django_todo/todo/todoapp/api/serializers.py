from rest_framework import serializers
from todoapp.models import Task

class TaskSerializer(serializers.ModelSerializer): # similar to forms.ModelForm
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

    def validate_title(self, value):
        ''' Checks whether the title is already in use '''
        ts = Task.objects.filter(title__iexact=value) # includes the current instance so it is always wrong
        if self.instance:
            ts = ts.exclude(pk=self.instance.pk)
        if ts.exists():
            raise serializers.ValidationError("This title has been taken")
        return value

class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'pk', 'title'
        ]
    
# the serializers
# converts to json
# validations for data passed
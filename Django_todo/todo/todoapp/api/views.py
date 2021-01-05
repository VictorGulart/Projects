# generic
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend # this will filter the models
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter # this will filter specified fields 
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import generics, mixins

from todoapp.models import Task

from .serializers import TaskSerializer 
from .permissions import IsOwnerOrReadOnly


class TaskPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

   
class TaskListView(generics.ListAPIView):
    ''' Just return a list of the task available
    Filters and Search can be added to upgrade query
    '''
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    # adding filters
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_fields = ('id', )
    search_fields = ('title', 'message', )

    # addding pagination
    pagination_class = TaskPagination



class TaskCreateView(generics.CreateAPIView):
    ''' Create new tasks '''
    lookup_field = 'pk' # this could be a slug or ID
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        # same as setting the queryset variable
        return Task.objects.all()

class TaskDestroyView(generics.DestroyAPIView):
    ''' Delete tasks 
    Also when deleting tasks may also mean that alll cache related to that 
    task must be cleared
    '''
    queryset = Task.objects.all()
    lookup_field = 'pk'


    # override the delete method to delete the cache
    def delete( self, request, *args, **kwargs):
        task_id = request.data.get('id') 
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache
            cache.delete(f'task_data_{task_id}')
        return response



class TaskListMixinView(mixins.CreateModelMixin, generics.ListAPIView):
    ''' It returns the same as a List but with the extra functionality to add content  '''
    lookup_field = 'pk' # this could be a slug or ID
    serializer_class = TaskSerializer
    
    #open permissions mean all permissions are valid
    # permission_classes = [] # they can be changed to authorize, but don't use very often
    def get_queryset(self):
        # same as setting the queryset variable
        # setting up the search for query example

        ts = Task.objects.all()
        query = self.request.GET.get('content')
        if query is not None:
            ts = ts.filter(
                Q(title__icontains=query) |
                Q(message__icontains=query)
            ).distinct() # distintic here is for unique
        return ts 
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    # Here we would also add this methods to handle edits
    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
    
    # def post(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
    

class TaskRUDView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView 
    ''' 
    RUD here stands for Retrieve Update Destroy
    This allows the user to get, update and delete the task  '''
    # default lookup field is the pk
    lookup_field = 'pk' # this could be a slug or ID
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnly]
    # queryset = Task.objects.all() 

    def get_queryset(self):
        # same as setting the queryset variable
        return Task.objects.all()
    
    # def get_object(self):
        # this overrides the default lookup_field
        # pk = self.kwargs.get('pk')
        # return Task.objects.get(pk=pk)
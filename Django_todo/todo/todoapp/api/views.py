# generic
from django.db.models import Q
from rest_framework import generics, mixins
from todoapp.models import Task
from .serializers import TaskListSerializer, TaskSerializer 
from .permissions import IsOwnerOrReadOnly


class ToDoAPIView(generics.CreateAPIView):
    lookup_field = 'pk' # this could be a slug or ID
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        # same as setting the queryset variable
        return Task.objects.all()

    # Adding the option to add a post form the list view api
    def post(self, request, *args, **kwargs):
        # this is the hardcoded way, instead we can use mixins
        return #
    
class ToDoListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class ToDoListViewMixin(mixins.CreateModelMixin, generics.ListAPIView):
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
    



class ToDoView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView 
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
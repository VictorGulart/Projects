from .views import ToDoView, ToDoAPIView, ToDoListView, ToDoListViewMixin
from django.urls import path

urlpatterns = [
    path('', ToDoListView.as_view(), name='taskList'),
    path('create', ToDoAPIView.as_view(), name='postCreate'), 
    path('list_edit', ToDoListViewMixin.as_view(), name='editList'),
    path('<int:pk>', ToDoView.as_view(), name='apimain')
]
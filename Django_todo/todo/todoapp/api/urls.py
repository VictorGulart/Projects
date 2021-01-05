from .views import TaskDestroyView, TaskListView, TaskCreateView, TaskListMixinView, TaskRUDView
from django.urls import path

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('new', TaskCreateView.as_view(), name='create_task'), 
    path('<int:pk>/destroy', TaskDestroyView.as_view(), name='destroy_task'),
    path('list_edit', TaskListMixinView.as_view(), name='edit_list'),
    path('<int:pk>', TaskRUDView.as_view(), name='detail_task')
]
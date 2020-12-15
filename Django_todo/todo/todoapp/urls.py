from django.urls import path, reverse
from django.urls.conf import include
from .views import add_task, delete_view, home_view, edit_view, list_view, edit_modal_view, get_modal_view

app_name = 'todoapp'
urlpatterns = [
        path('', home_view),
        path('list', list_view, name='show_list'),
        path('add_task', add_task, name='add_task'),
        path('edit/<int:pk>', edit_view, name='update_task'),
        path('get_modal/<int:pk>', get_modal_view, name='update_modal_task'),
        path('edit_modal_task/<int:pk>', edit_modal_view, name='update_modal_task'),
        path('<int:pk>/delete/', delete_view, name='delete_task')
        ]

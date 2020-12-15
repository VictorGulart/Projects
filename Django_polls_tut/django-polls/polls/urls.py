from django.urls import path
from . import views


'''
path() receives four args, two required route and view, and two optional kwargs and name
route - is a string that contains a URL pattern. django start at the beginning of the list
    and goes down comparing the requested url against each pattern until it finds one matching.
view - after finding a matching pattern, it calls the specified view function with a HTTPRequest

kwargs
name - naming the url let's I refer to it from anywhere in django, especially from
    within templates. It allows to make global changes to the URLS patterns of the 
    project while touching a single file

app_name - creates a namespace to make it easier to identify which view am I looking for
    for example we my have more than one app in the project with the same view function
    so to differentiate whe need this
'''

app_name = 'polls' # now we can add to the html page polls:detail to know we want this view
urlpatterns = [
        path('', views.IndexView.as_view(), name='index'), # this and home point to the same view
        path('home', views.IndexView.as_view(), name='index'), 
        path('<int:pk>/', views.DetailView.as_view(), name='detail'), # using generic views 
        path('<int:pk>/results/', views.ResultsView.as_view(), name='results'), # using generic views 
        path('<int:pk>/vote/', views.vote, name='vote')
        ]


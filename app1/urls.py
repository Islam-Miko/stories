from django.urls import path
from . import views
from app1.auxilary_functions import testing


urlpatterns = [
    path('story/all/', views.show_all_projects, name='some'),
    path('story/all/<int:subs_id>/',
         views.show_project_stories, name='project_stories'),
    path('story/all/all/<int:subs_id>/', testing, name='some'),
]
from django.urls import path
from . import views


urlpatterns = [
    path('story/all/', views.show_all_projects, name='some'),
    path('story/all/<int:subs_id>/',
         views.show_project_stories, name='project_stories'),
]
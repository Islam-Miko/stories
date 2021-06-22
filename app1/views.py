from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app1.auxilary_functions import *


@api_view(['GET'])
def show_all_projects(request):
    """just for testing"""
    query_today_active_projects = Story.objects.filter(end_date__gt=datetime.now()).values('id',
                                                                                           'preview',
                                                                                           'project_id__name')

    return Response(query_today_active_projects, status=status.HTTP_200_OK)


@api_view(['GET'])
def show_project_stories(request, subs_id):
    """Shows all categories for story"""
    active_stories_for_today, watched_stories_for_today = find_active_for_today_story_files(subs_id)
    result = mark_watched_stories(active_stories_for_today, watched_stories_for_today)
    return Response(result, status=status.HTTP_200_OK)
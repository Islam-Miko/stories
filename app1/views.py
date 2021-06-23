from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app1.auxilary_functions import *
from .serializers import StoryFileSerializer

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
    result_sorted_order = sort_by_order_num(active_stories_for_today)
    result = mark_watched_stories(result_sorted_order, watched_stories_for_today)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def show_stories(request,story_id, subs_id):
    all_project_sories = StoryFile.objects.filter(
        Q(story=story_id) & Q(end_date__gt=datetime.now()) &
        Q(start_date__lt=datetime.now())
    )
    serializer = StoryFileSerializer(all_project_sories, many=True)
    return Response(serializer.data)
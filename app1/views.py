from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app1.auxilary_functions import *
from .serializers import StoryFileSerializer, UserStoryInfoSer, StoryFileSerializer2


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


# @api_view(['GET'])
# def show_stories(request,story_id, subs_id):
#     all_project_sories = StoryFile.objects.filter(
#         Q(story=story_id) & Q(end_date__gt=datetime.now()) &
#         Q(start_date__lt=datetime.now())
#     )
#     earliest_date = min(all_project_sories, key=lambda i: i.start_date)
#
#     all_watched_stories = UserStoryInfo.objects.filter(
#         Q(user_story_file__story=story_id) &
#         Q(subs=subs_id) &
#         Q(watch_date__range=(earliest_date.start_date, datetime.now()))
#     )
#
#     project_query =
#     new_res= dict()
#     for watched_story in all_watched_stories:
#         for project_story in all_project_sories:
#             if watched_story.user_story_file == project_story.id:
#                 new_res.setdefault(project_story.id, dict())
#                 new_res[project_story.id][project_story]
#     print('ok')
#     print(new_res)
#
#
#
#     # ser2 = StoryFileSerializer2(all_project_sories, many=True)
#     # print(ser2.data)
#
#
#
#
#     ser = UserStoryInfoSer(all_watched_stories, many=True)
#     serializer = StoryFileSerializer(all_project_sories, many=True)
#     return Response((serializer.data, ser.data))


@api_view(['GET'])
def show_stories(request,story_id, subs_id):
    all_project_sories = StoryFile.objects.filter(
        Q(story=story_id) & Q(end_date__gt=datetime.now()) &
        Q(start_date__lt=datetime.now())
    ).values('id', 'detailedUrl', 'detailedText',
             'content_type', 'content',
             'duration', 'start_date')
    earliest_date = min(all_project_sories, key=lambda i: i['start_date'])
    all_watched_stories = UserStoryInfo.objects.filter(
        Q(user_story_file__story=story_id) &
        Q(subs=subs_id) &
        Q(watch_date__range=(earliest_date['start_date'], datetime.today()))
    ).values('user_story_file')


    if all_watched_stories:
        for project_story in all_project_sories:
            active_id = project_story['id']
            project_story['is_watched'] = False
            project_story.pop('start_date')
            project_story.pop('id')
            for watched_story in all_watched_stories:
                watched_id = watched_story['user_story_file']
                if watched_id == active_id:
                    project_story['is_watched'] = True
    else:
        for project_story in all_project_sories:
            project_story['is_watched'] = False
            project_story.pop('start_date')
            project_story.pop('id')



    return Response(all_project_sories)
from datetime import datetime

from django.db.models import Count, Q
from .models import *


def find_active_for_today_story_files(subs_id):
    active_stories_for_today = StoryFile.objects.filter(
        end_date__gt=datetime.now()).values(
        'story', 'story__preview', 'story__order_num', 'story__project__name').annotate(amt=Count('id'))
    watched_stories_for_today = UserStoryInfo.objects.filter(
        Q(subs=subs_id) &
        Q(user_story_file__end_date__gt=datetime.now())
    ).values('user_story_file__story').annotate(amt=Count('id', distinct=True))

    return active_stories_for_today, watched_stories_for_today


def create_new_sub_dict(key, will_be_showed, preview, name):
    if key not in will_be_showed:
        will_be_showed.setdefault(key, dict())
        will_be_showed[key]['preview'] = preview
        will_be_showed[key]['watched_all'] = False
        will_be_showed[key]['project'] = name


def mark_watched_stories(active_stories, watched_stories):
    """marks watched categories of stories"""
    will_be_showed = dict()
    if len(watched_stories) < 1:
        for active_story in active_stories:
            story = active_story['story']
            name = active_story['story__project__name']
            preview = active_story['story__preview']
            create_new_sub_dict(story, will_be_showed, preview, name)
        return will_be_showed
    for watched_story in watched_stories:
        watched_story_id = watched_story['user_story_file__story']
        watched_story_amount = watched_story['amt']
        for active_story in active_stories:
            story = active_story['story']
            amount = active_story['amt']
            name = active_story['story__project__name']
            preview = active_story['story__preview']
            create_new_sub_dict(story, will_be_showed, preview, name)
            if watched_story_id == story and watched_story_amount == amount:
                will_be_showed[story]['watched_all'] = True
    return will_be_showed


def sort_by_order_num(arr_dict):
    """sorts given dict accordingly to their order num (priority)"""
    result = sorted(arr_dict, key=lambda i: i['story__order_num'])
    return result


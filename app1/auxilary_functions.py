from datetime import datetime

from django.db.models import Count, Q
from rest_framework.decorators import api_view
from .models import *
from rest_framework.response import Response


def find_active_for_today_story_files(subs_id):
    active_stories_for_today = StoryFile.objects.filter(
        end_date__gt=datetime.now()).values(
        'story', 'story__preview').annotate(amt=Count('id'))
    watched_stories_for_today = UserStoryInfo.objects.filter(
        Q(subs=subs_id) &
        Q(user_story_file__end_date__gt=datetime.now())
    ).values('user_story_file__story').annotate(amt=Count('id', distinct=True))

    return active_stories_for_today, watched_stories_for_today


def create_new_sub_dict(key, will_be_showed, preview):
    if key not in will_be_showed:
        will_be_showed.setdefault(key, dict())
        will_be_showed[key]['preview'] = preview
        will_be_showed[key]['watched_all'] = False


def mark_watched_stories(active_stories, watched_stories):
    """marks watched categories of stories"""
    will_be_showed = dict()
    if len(watched_stories) < 1:
        for active_story in active_stories:
            story = active_story['story']
            preview = active_story['story__preview']
            create_new_sub_dict(story, will_be_showed, preview)
        return will_be_showed
    for watched_story in watched_stories:
        watched_story_id = watched_story['user_story_file__story']
        watched_story_amount = watched_story['amt']
        for active_story in active_stories:
            story = active_story['story']
            amount = active_story['amt']
            preview = active_story['story__preview']
            create_new_sub_dict(story, will_be_showed, preview)
            if watched_story_id == story and watched_story_amount == amount:
                will_be_showed[story]['watched_all'] = True
    return will_be_showed


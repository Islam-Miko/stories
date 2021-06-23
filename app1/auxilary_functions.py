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


def find_active_project_stories(story_id):
    all_project_stories = StoryFile.objects.filter(
        Q(story=story_id) & Q(end_date__gt=datetime.now()) &
        Q(start_date__lt=datetime.now())
    ).values('id', 'detailedUrl', 'detailedText',
             'content_type', 'content',
             'duration', 'start_date')
    return all_project_stories


def find_date_of_earlies_start(stories):
    early_story = min(stories, key=lambda i: i['start_date'])
    return early_story['start_date']


def find_watched_stories_by_subs(subs, earliest_date):
    subs_watched_stories = UserStoryInfo.objects.filter(
        Q(user_story_file__story=subs) &
        Q(subs=subs) &
        Q(watch_date__range=(earliest_date, datetime.today()))
    ).values('user_story_file')
    return subs_watched_stories


def find_active_and_watched_stories(story_id, subs_id):
    all_project_sories = find_active_project_stories(story_id)
    earliest_date = find_date_of_earlies_start(all_project_sories)
    all_watched_stories = find_watched_stories_by_subs(subs_id, earliest_date)
    return all_project_sories, all_watched_stories


def mark_stories_isWatched(all_stories, all_watched_stories):
    if all_watched_stories:
        for project_story in all_stories:
            active_id = project_story['id']
            project_story['is_watched'] = False
            project_story.pop('start_date')
            project_story.pop('id')
            for watched_story in all_watched_stories:
                watched_id = watched_story['user_story_file']
                if watched_id == active_id:
                    project_story['is_watched'] = True
    else:
        for project_story in all_stories:
            project_story['is_watched'] = False
            project_story.pop('start_date')
            project_story.pop('id')
from datetime import datetime

from .models import *


def find_active_for_today_story_files(subs_id):
    """searches in DB for active stories- total and watched by given id(viewer)
    returns to queries"""
    active_stories_for_today = StoryFile.objects.filter(end_date__gt=datetime.now()).values('story__preview', 'id',
                                                                                            'story')
    watched_stories_for_today = UserStoryInfo.objects.filter(
        subs=subs_id).values('user_story_file', 'user_story_file__id',
                                                'is_watched')
    return active_stories_for_today, watched_stories_for_today


def mark_watched_stories(active_stories, watched_stories):
    """marks watched categories of stories"""
    will_be_showed = dict()
    for watched_story in watched_stories:
        for active_story in active_stories:
            preview = active_story['story__preview']
            category_story_id = active_story['story']
            active_story_id = active_story['id']

            if category_story_id not in will_be_showed:
                will_be_showed.setdefault(category_story_id, dict())
                will_be_showed[category_story_id]['preview'] = preview

            if watched_story['user_story_file__id'] == active_story_id:
                will_be_showed[category_story_id]['watched'] = True
    return will_be_showed

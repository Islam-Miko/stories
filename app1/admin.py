from django.contrib import admin
from .models import Story, StoryFile, Subs, UserStoryInfo, Project

# Register your models here.
admin.site.register(Story)
admin.site.register(StoryFile)
admin.site.register(Subs)
admin.site.register(UserStoryInfo)
admin.site.register(Project)

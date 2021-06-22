from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField('Name', max_length=50)
    description = models.TextField('Description')


class Story(models.Model):
    preview = models.ImageField(verbose_name='Icon')
    start_date = models.DateTimeField(verbose_name='Start date')
    addDate = models.DateTimeField(verbose_name='DA', auto_now_add=True)
    order_num = models.IntegerField(verbose_name='Duration')
    project_id = models.ForeignKey(Project, verbose_name='Project', on_delete=models.CASCADE)
    end_date = models.DateTimeField(verbose_name='End date')


class StoryFile(models.Model):
    detailedUrl = models.URLField(verbose_name='More detUrl')
    detailedText = models.TextField(verbose_name='More Text')
    content_type = models.CharField(verbose_name='Content type', max_length=20)
    content = models.URLField(verbose_name='URL')
    duration = models.IntegerField('Duration')
    story_id = models.ForeignKey(Story, on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name='start date')
    end_date = models.DateTimeField(verbose_name='end date')


class UserStoryInfo(models.Model):
    story_file_id = models.ForeignKey(StoryFile, on_delete=models.CASCADE)
    subs_id = models.ForeignKey('Subs', on_delete=models.CASCADE)
    is_watched = models.FloatField(verbose_name='Watched', default=False)
    watch_date = models.DateTimeField(verbose_name='Watched')


class Subs(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
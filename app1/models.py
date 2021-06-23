from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField('Name', max_length=50)
    description = models.TextField('Description')

    def __str__(self):
        return self.name


class Story(models.Model):
    preview = models.ImageField(verbose_name='Icon', upload_to='app1/media/images')
    start_date = models.DateTimeField(verbose_name='Start date')
    addDate = models.DateTimeField(verbose_name='DA', auto_now_add=True)
    order_num = models.IntegerField(verbose_name='Order Priority')
    project = models.ForeignKey(Project, verbose_name='Project', on_delete=models.CASCADE)
    end_date = models.DateTimeField(verbose_name='End date')

    def __str__(self):
        return f'{self.id}'


class StoryFile(models.Model):
    detailedUrl = models.URLField(verbose_name='More detUrl')
    detailedText = models.TextField(verbose_name='More Text')
    content_type = models.CharField(verbose_name='Content type', max_length=20)
    content = models.URLField(verbose_name='URL')
    duration = models.IntegerField('Duration')
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name='start date')
    end_date = models.DateTimeField(verbose_name='end date')

    def __str__(self):
        return f'{self.id} story file'


class UserStoryInfo(models.Model):
    user_story_file = models.ForeignKey(StoryFile, on_delete=models.CASCADE)
    subs = models.ForeignKey('Subs', on_delete=models.CASCADE)
    is_watched = models.BooleanField(verbose_name='Watched', default=False)
    watch_date = models.DateTimeField(verbose_name='Watched')

    def __str__(self):
        return f'{self.id}'


class Subs(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
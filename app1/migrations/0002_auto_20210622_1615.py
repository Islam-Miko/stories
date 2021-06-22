# Generated by Django 3.2.4 on 2021-06-22 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='story',
            old_name='project_id',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='storyfile',
            old_name='story_id',
            new_name='story',
        ),
        migrations.RenameField(
            model_name='userstoryinfo',
            old_name='story_file_id',
            new_name='story_file',
        ),
        migrations.RenameField(
            model_name='userstoryinfo',
            old_name='subs_id',
            new_name='subs',
        ),
        migrations.AlterField(
            model_name='userstoryinfo',
            name='is_watched',
            field=models.BooleanField(default=False, verbose_name='Watched'),
        ),
    ]

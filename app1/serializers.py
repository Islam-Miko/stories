from rest_framework import serializers

from .models import StoryFile, UserStoryInfo, Story

class StoryFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryFile
        fields = (
            'id',
            'detailedUrl',
            'detailedText',
            'content_type',
            'content',
            'duration',
        )


class StoryFileSerializer2(serializers.ModelSerializer):
    class Meta:
        model = StoryFile
        fields = (
            'id',
            'detailedUrl',
            'detailedText',
            'content_type',
            'content',
            'duration',
            'is_watched',
        )

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'

class UserStoryInfoSer(serializers.ModelSerializer):
    class Meta:
        model = UserStoryInfo
        fields = '__all__'
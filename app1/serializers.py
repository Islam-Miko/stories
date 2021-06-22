from rest_framework import serializers

from .models import StoryFile, UserStoryInfo, Story

class StoryFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryFile
        fields = '__all__'


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'


class UserStoryInfoSer(serializers.ModelSerializer):
    class Meta:
        model = UserStoryInfo
        fields = '__all__'
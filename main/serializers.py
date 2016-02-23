from models import Event, Song, CmsUser, Like
from rest_framework import serializers

BASE_READONLY_FIELDS = [
    'order',
    'uid',
    'created',
    'modified',
]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CmsUser
        exclude = ['user_permissions', 'groups']


class SongSerializer(serializers.HyperlinkedModelSerializer):
    likes = serializers.IntegerField(source='like_set.count', read_only=True)

    class Meta:
        model = Song
        fields = ('title', 'event', 'cmsUser', 'likes', 'uid')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Event


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        exclude = ['order']

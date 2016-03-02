from django.core.exceptions import ObjectDoesNotExist
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


class SongSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source='like_set.count', read_only=True)
    liked = serializers.SerializerMethodField('is_liked')

    def is_liked(self, song):
        try:
            like = Like.objects.get(cmsUser=self.context['request'].user, song=song)
            return like.id
        except Exception:
            return -1

    class Meta:
        model = Song


class EventSerializer(serializers.HyperlinkedModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Event


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event


class LikeSerializer(serializers.ModelSerializer):
    cmsUser = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Like
        exclude = ['order']

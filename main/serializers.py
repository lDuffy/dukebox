from models import AppUser, Event, Song, CmsUser
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField, empty

BASE_READONLY_FIELDS = [
    'order',
    'uid',
    'created',
    'modified',
]


class UserSerializer(serializers.ModelSerializer):
    email = ReadOnlyField()

    class Meta:
        model = CmsUser
        exclude = ['password']


class AppUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AppUser
        read_only_fields = BASE_READONLY_FIELDS + [
            'publish',
        ]

    def __init__(self, instance=None, data=empty, **kwargs):
        super(AppUserSerializer, self).__init__(instance, data, **kwargs)

    def update(self, instance, validated_data):
        user = instance.user

        user_data = validated_data.pop('user')
        # only first and last name is allowed to change
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()

        return super(AppUserSerializer, self).update(instance, validated_data)


class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song
        fields = ('title', 'count', 'chosen')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Event

from models import  Event, Song, CmsUser
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
        fields = ('id', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CmsUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user

    def __init__(self, instance=None, data=empty, **kwargs):
        super(UserSerializer, self).__init__(instance, data, **kwargs)

    def update(self, instance, validated_data):
        user = instance.user

        user_data = validated_data.pop('user')
        # only first and last name is allowed to change
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.save()

        return super(UserSerializer, self).update(instance, validated_data)


class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song
        fields = ('title', 'count', 'chosen')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Event


class EventListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event

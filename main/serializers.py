from models import  Event, Song, CmsUser
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
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def create(self, validated_data):
        user = CmsUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.username = validated_data['username']
        user.save()

        return user

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

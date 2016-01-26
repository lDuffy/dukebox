from models import Event, Song, CmsUser
from rest_framework import serializers
from rest_framework.authtoken.models import Token

BASE_READONLY_FIELDS = [
    'order',
    'uid',
    'created',
    'modified',
]


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data, *args, **kwargs):
        user = CmsUser.objects.create(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username']
        )

        user.save()
        user.token = Token.objects.create(user=user)
        user.save()

        return user

    class Meta:
        model = CmsUser
        exclude = ['user_permissions', 'groups']


class SongSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Song
        exclude = ["modified", "created", "uid", "url"]


class EventSerializer(serializers.HyperlinkedModelSerializer):
    songs = SongSerializer(many=True)

    class Meta:
        model = Event


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event

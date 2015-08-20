from models import AppUser, Event, Song
from permissions import IsAppUser
from rest_framework import viewsets
from serializers import  EventSerializer, SongSerializer, AppUserSerializer


class AppUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AppUser to be viewed or edited.
    """
    permission_classes = (IsAppUser,)
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Event to be viewed or edited.
    """
    permission_classes = (IsAppUser,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Event to be viewed or edited.
    """
    permission_classes = (IsAppUser,)
    queryset = Song.objects.all()
    serializer_class = SongSerializer


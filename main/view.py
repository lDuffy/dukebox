from models import  Event, Song, CmsUser
from permissions import IsAppUser, IsOwnerOrReadOnly
from rest_framework import viewsets
from serializers import  EventSerializer, SongSerializer,  EventListSerializer, UserSerializer


class CmsUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AppUser to be viewed or edited.
    """
    # permission_classes = (IsAppUser,)
    queryset = CmsUser.objects.all()
    serializer_class = UserSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Event to be viewed or edited.
    """
    permission_classes = (IsAppUser, IsOwnerOrReadOnly,)
    queryset = Event.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        if self.action == 'retrieve':
            return EventSerializer
        return EventListSerializer


class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Event to be viewed or edited.
    """
    permission_classes = (IsAppUser,)
    queryset = Song.objects.all()
    serializer_class = SongSerializer


from gcm.api import GCMMessage
from models import Event, Song, CmsUser, Like
from permissions import IsAppUser
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from serializers import EventSerializer, SongSerializer, EventListSerializer, UserSerializer, LikeSerializer


# API endpoint that allows Models to be viewed or edited.


class CmsUserViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAppUser,)
    queryset = CmsUser.objects.all()
    serializer_class = UserSerializer


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAppUser,)
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @detail_route(methods=['post'])
    def checkin_user(self, request, pk=None):
        user = request.user
        event = Event.objects.get(id=pk)

        cms_user = CmsUser.objects.get(username=user.username)
        cms_user.checked_in_event = event
        cms_user.save()
        return Response({'status': 'checked in'})

    @detail_route(methods=['post'])
    def checkout_user(self, request, pk=None):
        user = request.user
        cms_user = CmsUser.objects.get(username=user.username)

        cms_user.checked_in_event = None
        cms_user.save()
        return Response({'status': 'checked out'})

    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        if self.action == 'retrieve':
            return EventSerializer
        return EventListSerializer

    def perform_create(self, serializer):
        user = self.request.user
        cms_user = CmsUser.objects.get(username=user.username)
        serializer.save(creator=cms_user)

    @detail_route(methods=['post'])
    def play(self, request, pk=None):

        cms_user = CmsUser.objects.get(username=request.user.username)
        event = cms_user.checked_in_event
        songs = Song.objects.all().filter(event=event)

        try:
            current_song = songs.get(playback_status=Song.PLAYING)
            if current_song:
                current_song.playback_status = Song.PLAYED
                current_song.save()
        except Song.DoesNotExist:
            pass

        try:
            next_song = songs.get(provider_id=request.query_params.get('song_id', None))
            if next_song:
                next_song.playback_status = Song.PLAYING
                next_song.save()
                self.send_gcm_message(pk)
                return Response({'status': 'playing' + pk})
        except Song.DoesNotExist:
            return Response({'error': 'invalid song id' + pk})

    @detail_route(methods=['get'])
    def pause(self, request, pk=None):

        cms_user = CmsUser.objects.get(username=request.user.username)
        event = cms_user.checked_in_event
        songs = Song.objects.all().filter(event=event)

        try:
            current_song = songs.get(playback_status=Song.PLAYING)
            if current_song:
                current_song.playback_status = Song.PAUSED
                current_song.save()
                self.send_gcm_message(pk)
                return Response({'status': 'paused'})
        except Song.DoesNotExist:
            pass

        try:
            current_song = songs.get(playback_status=Song.PAUSED)
            if current_song:
                current_song.playback_status = Song.PLAYING
                current_song.save()
                self.send_gcm_message(pk)
                return Response({'status': 'playing'})
        except Song.DoesNotExist:
            pass

    def send_gcm_message(self, pk):
        try:
            topic = "/topics/" + str(self.request.user.checked_in_event.pk)
            GCMMessage().send({'message': 'event' + pk}, to=topic)
        except Exception:
            pass


class SongViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAppUser,)
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def perform_create(self, serializer):
        serializer.save(event=self.request.user.checked_in_event, cmsUser=self.request.user)

        topic = "/topics/" + str(self.request.user.checked_in_event.pk)
        GCMMessage().send({'message': 'my test message'}, to=topic)


class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAppUser,)
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

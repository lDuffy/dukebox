from main.models import CmsUser, Event, Song

__author__ = 'centralstation'


def setup_content():
    user_one = CmsUser.objects.create_user("x@y.com", "pass")
    user_two = CmsUser.objects.create_user("y@y.com", "pass")
    event_one = Event.objects.create(title="twisetd pepper", creator=user_one,)
    event_two = Event.objects.create(title="sugar club", creator=user_two,)


    Song.objects.create(title="ghetto life", event=event_one, cmsUser=user_one)
    Song.objects.create(title="rock you baby", event=event_one, cmsUser=user_two)

    Song.objects.create(title="ghetto life", event=event_two, cmsUser=user_one)
    Song.objects.create(title="rock you baby", event=event_two, cmsUser=user_two)


def run():
    setup_content()

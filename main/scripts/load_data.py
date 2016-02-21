from main.models import CmsUser, Event, Song

__author__ = 'centralstation'


def setup_content():
    user_one = CmsUser.objects.create_user(username="x@y.com", email="x@y.com", password="pass")
    user_one.is_staff = True
    user_one.is_superuser = True
    user_one.save()
    user_two = CmsUser.objects.create_user(username="a@ya.com", email="a@ya.com", password="pass")
    event_one = Event.objects.create(title="twisetd pepper", creator=user_one, )
    event_two = Event.objects.create(title="sugar club", creator=user_two, )

    Song.objects.create(title="ghetto life", event=event_one, cmsUser=user_one)
    Song.objects.create(title="rock you baby", event=event_one, cmsUser=user_two)

    Song.objects.create(title="ghetto life", event=event_two, cmsUser=user_one)
    Song.objects.create(title="rock you baby", event=event_two, cmsUser=user_two)


def run():
    setup_content()

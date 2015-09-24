from django.contrib import admin
from models import CmsUser, Event, Song


class CmsUserAdmin(admin.ModelAdmin):

    save_on_top = True


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'cmsUser']
    save_on_top = True


class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'event', 'cmsUser']
    save_on_top = True


admin.site.register(CmsUser, CmsUserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Song, SongAdmin)

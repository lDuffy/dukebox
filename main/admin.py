from django.contrib import admin
from models import CmsUser, Event, Song, Like


class CmsUserAdmin(admin.ModelAdmin):
    list_display = ['username']
    save_on_top = True


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator']
    save_on_top = True


class LikesInLine(admin.TabularInline):
    model = Like
    extra = 0


class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'event', 'cmsUser']
    save_on_top = True

    inlines = [
        LikesInLine
    ]


class LikeAdmin(admin.ModelAdmin):
    list_display = ['song']
    save_on_top = True


admin.site.register(CmsUser, CmsUserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Like, LikeAdmin)

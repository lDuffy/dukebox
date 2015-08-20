from django.contrib import admin
from models import AppUser, Event, Song


class AppUserAdmin(admin.ModelAdmin):

    save_on_top = True


class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'appUser']
    save_on_top = True


class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'event', 'appUser']
    save_on_top = True


admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Song, SongAdmin)

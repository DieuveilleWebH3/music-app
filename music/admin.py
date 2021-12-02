from django.contrib import admin
from .models import *


# Register your models here.

class GenreAdmin(admin.ModelAdmin):
    list_display = ("title", "logo")
    list_filter = ("title", )
    search_fields = ("title",)

    prepopulated_fields = {'slug': ('title',)}


class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "artist", "genres", "is_favorites", "user", "album_logo")
    list_filter = ("genre", "artist")
    search_fields = ("title", "artist", "genre")

    prepopulated_fields = {'slug': ('title',)}

    def genres(self, obj):
        return "\n".join([genre.title + ', ' for genre in obj.is_favorite.all()])

    def is_favorites(self, obj):
        return "\n".join([user.username + ', ' for user in obj.is_favorite.all()])


class SongAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "album", "is_favorites")
    list_filter = ("album",)
    search_fields = ("title",)

    prepopulated_fields = {'slug': ('title',)}

    def is_favorites(self, obj):
        return "\n".join([user.username + ', ' for user in obj.is_favorite.all()])


class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "user", "songs")
    list_filter = ("user",)
    search_fields = ("title",)

    prepopulated_fields = {'slug': ('title',)}

    def songs(self, obj):
        return "\n".join([song.title + ', ' for song in obj.is_favorite.all()])


admin.site.register(Song, SongAdmin)

admin.site.register(Album, AlbumAdmin)

admin.site.register(Genre, GenreAdmin)

admin.site.register(Playlist, PlaylistAdmin)


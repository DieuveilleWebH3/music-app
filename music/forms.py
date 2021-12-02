from django import forms
from django.contrib.auth.models import User
from .models import *


class GenreForm(forms.ModelForm):

    class Meta:
        model = Genre
        fields = ['title', ]
        labels = {
            "title": "Genre Name",
        }


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'title', 'genre', 'album_logo']
        labels = {
            "title": "Album Name",
        }


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['title', 'audio_file']
        labels = {
            "title": "Song Name",
        }


class PlaylistForm(forms.ModelForm):

    class Meta:
        model = Playlist
        fields = ['title', ]
        labels = {
            "title": "Playlist Name",
        }



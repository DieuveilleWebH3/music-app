from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic.edit import UpdateView
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from .forms import *
from .models import *

from django.utils.text import slugify
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib import messages
from django.views import View
from django.views.decorators.http import require_POST, require_GET
# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django import forms
from django.core import serializers


# Create your views here.


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def index(request):
    if request.user.is_active:

        return render(request, 'music/index.html',)
    else:

        return render(request, 'music/index.html')


def search(request):

    return render(request, 'music/search.html')


def detail(request, album_slug):
    if request.user.is_active:
        user = request.user
        album = get_object_or_404(Album, slug=album_slug)
        return render(request, 'music/detail.html', {'album': album, 'user': user})
    else:
        return render(request, 'music/base_visitor.html')


def create_album(request):
    form = AlbumForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        album = form.save(commit=False)
        album.user = request.user
        album.album_logo = request.FILES['album_logo']
        file_type = album.album_logo.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in IMAGE_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Image file must be PNG, JPG, or JPEG',
            }
            return render(request, 'music/album_form.html', context)
        album.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        "form": form,
    }
    return render(request, 'music/album_form.html', context)


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.filter(user=request.user)
    return render(request, 'music/index.html', {'albums': albums})


def create_song(request, album_slug):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, slug=album_slug)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/create_song.html', context)

        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/create_song.html', context)


def delete_song(request, album_slug, song_slug):
    album = get_object_or_404(Album, slug=album_slug)
    song = Song.objects.get(album=album, slug=song_slug)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})


def favorite(request, slug):
    song = get_object_or_404(Song, slug=slug)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, slug):
    album = get_object_or_404(Album, slug=slug)

    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def songs(request, filter_by):
    try:
        song_ids = []
        for album in Album.objects.filter(user=request.user):
            for song in album.song_set.all():
                song_ids.append(song.pk)
        users_songs = Song.objects.filter(pk__in=song_ids)
        if filter_by == 'favorites':
            users_songs = users_songs.filter(is_favorite=True)
    except Album.DoesNotExist:
        users_songs = []
    return render(request, 'music/songs.html', {
        'song_list': users_songs,
        'filter_by': filter_by,
    })




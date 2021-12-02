from django.db import models
from account.models import *
from django.contrib.auth.models import Permission
from django.urls import reverse

# Create your models here.


class Genre(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Album(models.Model):

    def get_upload_path(instance, filename):
        return 'artist/{0}/{1}'.format(instance.artist, filename)

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    artist = models.CharField(max_length=250)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    # genre = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre, blank=True, related_name='genres')
    album_logo = models.ImageField(upload_to=get_upload_path, blank=True)
    # is_favorite = models.BooleanField(default=False)
    is_favorite = models.ManyToManyField(User, blank=True, related_name='favorite_albums')

    def get_absolute_url(self):
        return reverse('music:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title + ' - ' + self.artist


class Song(models.Model):

    def get_upload_path(instance, filename):
        return 'artist/{0}/{1}'.format(instance.album.artist, filename)

    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    audio_file = models.FileField(upload_to=get_upload_path, null=False, blank=False)
    is_favorite = models.ManyToManyField(User, blank=True, related_name='favorite_songs')
    # is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Playlist(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    song = models.ManyToManyField(Song, blank=True, related_name='playlist_songs')
    # song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


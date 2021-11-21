from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import UpdateView
from django.http import JsonResponse
from django.db.models import Q
from .forms import *
from .models import *


# Create your views here.


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def index(request):
    if request.user.is_active:
        
        return render(request, 'music/index.html',)
    else:

        return render(request, 'music/index.html')


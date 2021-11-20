from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    
    # /music/
    url(r'^$', views.index, name='index'),

]
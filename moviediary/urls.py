'''
Created on 13 Mar 2016

@author: Neil
'''

from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^review_form/$', views.review_form, name='review_form'),
]
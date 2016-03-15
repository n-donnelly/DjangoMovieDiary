'''
Created on 13 Mar 2016

@author: Neil
'''

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
'''
Created on 13 Mar 2016

@author: Neil
'''

from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^search/$', views.search, name='search'),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>\w+)/reviews/$', views.profile_reviews, name='review_profiles'),
    url(r'^profile/(?P<movie_id>\w+)/$', views.get_movie_page, name='movie_page'),
    url(r'^review_form/$', views.review_form, name='review_form'),
    url(r'^review_submit/$', views.review_submit, name='review_submit'),
    url(r'^add_movie_to_wishlist/$', views.add_movie_to_wishlist, name='add_movie_to_wishlist'),
    url(r'^get_movie_info/$', views.get_movie_info, name="get_movie_info"),
    url(r'^add_test_data/$', views.add_test_data, name="add_test_data")
]
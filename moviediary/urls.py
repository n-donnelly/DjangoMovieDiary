'''
Created on 13 Mar 2016

@author: Neil
'''

from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, password_change

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^search/$', views.search, name='search'),
    url(r'^aboutus/$', views.about_us, name='about_us'),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', views.logout_view),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/password_change/$', password_change),
    url(r'^accounts/password_change_done/$', views.index, name="password_change_done"),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>\w+)/profile_edit/$', views.edit_profile, name='profile_edit'),
    url(r'^profile/(?P<username>\w+)/remove_user_page/$', views.remove_user_view, name='remove_user_view'),
    url(r'^profile/(?P<username>\w+)/remove_user/$', views.remove_user, name='remove_user'),
    url(r'^profile/(?P<username>\w+)/reviews/$', views.profile_reviews, name='review_profiles'),    
    url(r'^profile/(?P<username>\w+)/reviews/(?P<page>[0-9]+)/$', views.profile_reviews, name='review_profiles'),
    url(r'^profile/(?P<username>\w+)/wishlist/$', views.profile_wishlist, name='wishlist'),
    url(r'^profile/(?P<username>\w+)/wishlist/(?P<page>[0-9]+)/$', views.profile_wishlist, name='wishlist'),
    url(r'^movie/(?P<movie_id>\w+)/$', views.get_movie_info, name='movie_page'),
    url(r'^movie/(?P<movie_id>\w+)/reviews/$', views.get_movie_reviews, name='movie_reviews'),
    url(r'^review_form/$', views.review_form, name='review_form'),
    url(r'^review_submit/$', views.review_submit, name='review_submit'),
    url(r'^add_movie_to_wishlist/$', views.add_movie_to_wishlist, name='add_movie_to_wishlist'),
    url(r'^remove_movie_from_wishlist/$', views.remove_movie_from_wishlist, name='remove_movie_from_wishlist'),
    url(r'^get_movie_info/$', views.get_movie_info, name="get_movie_info"),
    url(r'^add_test_data/$', views.add_test_data, name="add_test_data"),
    url(r'^get_movie_ratings/$', views.get_movie_ratings, name="get_movie_ratings")
]
from __future__ import unicode_literals

import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Reviewer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    num_of_reviews=models.IntegerField('Number of Reviews', default=0)
    reset_token = models.CharField(max_length=12, default='')
    bio = models.TextField('Bio', default='')
    love_movie_text = models.TextField('Love Movies', default='')
    favourite_genres = models.TextField('Favourite Genres', default='')
    profile_pic = models.CharField(max_length=20, default='amelie.jpg')
    
    def __unicode__(self):
        return self.user
    
class Movie(models.Model):
    title=models.CharField(max_length=200)
    release_date = models.DateField('release date', default=datetime.date.today) 
    ext_id=models.CharField(max_length=64, default='0', unique=True)
    tagline=models.TextField('Tagline', default='')
    image_url = models.CharField(max_length=256, default='')
    num_of_reviews=models.IntegerField('Number of Reviews', default=0)
    average_review_score=models.FloatField('Average Review Score', default=0)
    
    def __unicode__(self):
        return self.title
    
class Review(models.Model):
    score = models.IntegerField('Review Score')
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE, related_name="rev_reviewers") 
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="rev_movies")
    review_text = models.TextField('Review Text', default='')
    review_headline=models.TextField("Review Headline", default='')
    review_date = models.DateField('Review Date', default=datetime.date.today)
    second_review = models.TextField('Second Impressions', default='')
    second_headline = models.TextField('Second Headline', default='')  
    second_rev_date = models.DateField('Second Impressions Date', default=datetime.date.today)
    
    def __unicode__(self):
        return u'%s reviewing %s' % (self.reviewer.user.username, self.movie.title)
    
class Following(models.Model):
    follower = models.ForeignKey(Reviewer, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(Reviewer, on_delete=models.CASCADE, related_name='following')
    follow_date = models.DateField('Date of Follow', default=datetime.date.today)
    
    def __unicode__(self):
        return u'%s following %s' % (self.follower.username, self.followed.username)
    
class Wishlist(models.Model):
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE, related_name="wish_reviewers")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="wish_movies")
    
    def __unicode__(self):
        return u'%s wants to see %s' % (self.user.username, self.movie.title)
    
from __future__ import unicode_literals

import datetime

from django.db import models


# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=200, unique=True)
    email=models.CharField(max_length=200, unique=True)
    salt=models.CharField(max_length=64, default='AAAA')
    hashed_password=models.CharField(max_length=256, default='')
    num_of_reviews=models.IntegerField('Number of Reviews', default=0)
    reset_token = models.CharField(max_length=12, default='')
    
    def __unicode__(self):
        return self.username
    
class Movie(models.Model):
    title=models.CharField(max_length=200)
    release_date = models.DateField('release date', default=datetime.date.today) 
    ext_id=models.CharField(max_length=64, default='0', unique=True)
    tagline=models.TextField('Tagline', default='')
    image_url = models.CharField(max_length=256, default='')
    
    def __unicode__(self):
        return self.title
    
class Review(models.Model):
    score = models.IntegerField('Review Score')
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review_text = models.TextField('Review Text', default='')
    review_date = models.DateField('Review Date', default=datetime.date.today)
    second_review = models.TextField('Second Impressions', default='')  
    second_rev_date = models.DateField('Second Impressions Date', default=datetime.date.today)
    
    def __unicode__(self):
        return u'%s reviewing %s' % (self.user.username, self.movie.title)
    
class Following(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follow_date = models.DateField('Date of Follow', default=datetime.date.today)
    
    def __unicode__(self):
        return u'%s following %s' % (self.follower.username, self.followed.username)
    
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
    def __unicode__(self):
        return u'%s wants to see %s' % (self.user.username, self.movie.title)
    
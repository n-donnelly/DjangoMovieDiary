from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    
class Movie(models.Model):
    title=models.CharField(max_length=200)
    release_date = models.DateTimeField('release date') 
    
class Review(models.Model):
    score = models.IntegerField('Review Score')
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review_text = models.TextField('Review Text');  
    
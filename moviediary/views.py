#from django.shortcuts import render
import re

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.context import Context
from django.utils.html import strip_tags

from moviediary.db_operations import getWishlistMovies, getReviewsForUser, \
    getCountOfFollowersForUser, getCountOfFollowedsForUser, \
    getReviewsFromFollowed
from moviediary.models import Reviewer
from moviediary.operations import op_signup


# Create your views here.
def index(request):
    context = {}
    return render(request, 'moviediary/index.html', context)

def signup(request, username, email, password):
    #See if username exists, if so get salt add to password and hash and see if it matches hashed_password
    return HttpResponse("Attempting to sign up with username: " + username)

def review(request, title, ext_id, poster_url, date_seen, tagline, score, review, user_id):
    #add movie to DB with title, ext_id, poster_url, date_seen, tagline
    #Create review from user id and movie id
    return HttpResponse("Attempting to review movie: " + title)

def register(request):
    username = strip_tags(request.POST.get('username', ''))
    password = strip_tags(request.POST.get('password', ''))
    email = strip_tags(request.POST.get('email', ''))
    
    if((re.match("^[a-zA-Z0-9_.-]+$",username) is None) or 
       User.objects.filter(username=username).exists() or
       User.objects.filter(email=email).exists()):
        context = Context({"error": "User already exists"})
        return render(request, 'registration/login.html')
        
    user = User.objects.create_user(username=username,
                                    email=email,
                                    password = password)
    
    op_signup(user)
    return render(request, 'moviediary/profile.html')

#TODO: Decide whether to take these out and move them to AJAX responses to reduce the 
#up front load cost of all these DB queries - okay for now but won't scale particularly well
#What's quicker - loads of DB calls up front or 3 different AJAX calls to fill in information
def profile(request):
    context = {}
    
    print(request.user)
    reviewer = get_object_or_404(Reviewer, user=request.user)
    context['reviewer'] = reviewer
    
    #Possibly limit as numbers get too big to reduce performance for these profile DB queries?
    context['wishlist'] = getWishlistMovies(reviewer)
    
    context['reviews'] = getReviewsForUser(reviewer)
    
    context['num_following'] = getCountOfFollowersForUser(reviewer)
    
    context['num_followed'] = getCountOfFollowedsForUser(reviewer)
    
    context['follow_reviews'] = getReviewsFromFollowed(reviewer)
    
    if request.user.is_authenticated():
        return render(request, 'moviediary/profile.html', context)
    else:
        return render(request, 'registration/login.html')
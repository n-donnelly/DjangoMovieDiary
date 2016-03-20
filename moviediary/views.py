#from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    context = {}
    return render(request, 'moviediary/index.html', context)

def login(request, username, password):
    # Create a random salt, add to password and hash. Add username, salt, hashed password and random reset token to DB
    return HttpResponse("Attempting to login with username: " + username)

def signup(request, username, password):
    #See if username exists, if so get salt add to password and hash and see if it matches hashed_password
    return HttpResponse("Attempting to sign up with username: " + username)

def review(request, title, ext_id, poster_url, date_seen, tagline, score, review, user_id):
    #add movie to DB with title, ext_id, poster_url, date_seen, tagline
    #Create review from user id and movie id
    return HttpResponse("Attempting to review movie: " + title)
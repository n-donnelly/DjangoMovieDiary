#from django.shortcuts import render
import re

from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.context import Context
from django.utils.html import strip_tags

from moviediary.db_operations import getWishlistMovies, getReviewsForUser, \
    getCountOfFollowersForUser, getCountOfFollowedsForUser, \
    getReviewsFromFollowed
from moviediary.models import Reviewer
from moviediary.operations import op_signup, op_addMovie, \
    op_removeMovieFromWishlist, op_addReview, op_addMovieToWishlist, op_getMovie, \
    op_getReview, op_isMovieWishlisted, op_fillTestData


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
        return render(request, 'registration/login.html', context)
        
    user = User.objects.create_user(username=username,
                                    email=email,
                                    password = password)
    
    op_signup(user)
    return render(request, 'moviediary/profile.html .movie_form')

#TODO: Decide whether to take these out and move them to AJAX responses to reduce the 
#up front load cost of all these DB queries - okay for now but won't scale particularly well
#What's quicker - loads of DB calls up front or 3 different AJAX calls to fill in information
def profile(request, username=''):
    context = {}
    
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
    
def review_form(request):
    return render(request, 'moviediary/review_form.html')

#Add movie to DB if not there
#Remove movie from user's wishlist
#Add review for movie and user
def review_submit(request):
    if request.user.is_authenticated():
        errors = {}
        errors['error'] = []
        if request.method == 'POST' and request.is_ajax():
            if not request.POST.get('headline'):
                errors['error'].append('Needs a headline')
            if not request.POST.get('review_text'):
                errors['error'].append('You need to write a review')
            if not request.POST.get('review_date'):
                errors['error'].append('Please give a date')
            if not request.POST.get('rating'):
                errors['error'].append('We need a rating')
            if not errors['error']:
                headline = request.POST.get('headline')
                review_text = request.POST.get('review_text')
                review_date = request.POST.get('review_date')
                rating = request.POST.get('rating')
                movie_title = request.POST.get('movie_title')
                movie_id = request.POST.get('movie_id')
                poster_url = request.POST.get('poster_url')
                release_date = request.POST.get('release_date')
                tagline = request.POST.get('tagline')
                reviewer = get_object_or_404(Reviewer, user=request.user)
                
                m = op_addMovie(movie_title,release_date,movie_id, tagline, poster_url)
                if m is 0:
                    op_removeMovieFromWishlist(m, reviewer)
                    
                r = op_addReview(reviewer, m, review_text, review_date, rating, headline)
                
                if r.startswith('Error'):
                    return JsonResponse({"review_status":r})
                else:
                    return JsonResponse({"review_status":"success"});
        errors['review_status'] = 'There were errors'
        return JsonResponse(errors)
    else:
        return render(request, 'registration/login.html')

#Add movie to wishlist for user    
def add_movie_to_wishlist(request):
    if request.user.is_authenticated():
        errors = {}
        errors['error'] = []
        if request.method == 'POST' and request.is_ajax():
            if not request.POST.get('movie_id'):
                errors['error'].append('Invalid movie id')
            if not errors['error']:
                movie_title = request.POST.get('movie_title')
                movie_id = request.POST.get('movie_id')
                poster_url = request.POST.get('poster_url')
                release_date = request.POST.get('release_date')
                tagline = request.POST.get('tagline')
                reviewer = get_object_or_404(Reviewer, user=request.user)
                
                m = op_addMovie(movie_title, release_date, movie_id, tagline, poster_url)
                w = op_addMovieToWishlist(reviewer, m);
                if w.startswith('Error'):
                    return JsonResponse({"wish_status":w})
                else:
                    return JsonResponse({"wish_status":"success"});
        errors['status'] = "Failed to add movie to user's wishlist";
        return JsonResponse(errors);
    else:
        return JsonResponse({"wish_status":"Not logged in"});
    
def get_movie_info(request):
    context = {}
    
    if request.is_ajax():
        m_id = request.GET.get('movie_id')
        m = op_getMovie(m_id)
        if m.startswith('Error'):
            return Http404
        context['movie'] = m
        
        if request.user.is_authenticated():
            reviewer = get_object_or_404(Reviewer, user=request.user)
            context['review'] = op_getReview(m,reviewer)
            context['wishlist'] = op_isMovieWishlisted(m,reviewer)
        return JsonResponse(context)
    else:
        raise Http404
    
def get_movie_page(request):
    context = {}
    
    m_id = request.GET.get('movie_id')
    m = op_getMovie(m_id)
    
    return render(request, 'moviediary/movie_page.html', context)

def add_test_data(request):
    if request.user.is_authenticated() and request.is_ajax():
        op_fillTestData()
        return JsonResponse({"status":"success"})
    else :
        raise Http404
#from django.shortcuts import render
import json
import re
import time
import types

from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404  
from django.template.context import Context
from django.utils.html import strip_tags

from moviediary.db_operations import getWishlistMoviesForReviewer, getReviewsForUser, \
    getCountOfFollowersForUser, getCountOfFollowedsForUser
from moviediary.models import Reviewer, Movie
from moviediary.operations import op_signup, op_addMovie, \
    op_removeMovieFromWishlist, op_addReview, op_addMovieToWishlist, op_getMovie, \
    op_getReview, op_isMovieWishlisted, op_fillTestData, \
    op_getMostRecentReviewsForMovie, op_normalizeMovieObject, \
    op_normalizeReviewObject, op_updateReviewerProfile, op_getReviewsForMovie, \
    op_getRecentReviews, op_getTopWishlistedMovies


def index(request):
    context = {}
    
    rec_revs = []
    reviews = op_getRecentReviews()
    for r in reviews:
        rec_revs.append(op_normalizeReviewObject(r))
        
    if len(rec_revs) > 0:
        context['recent_reviews'] = rec_revs;
        
    wish_movs = []
    w_movies = op_getTopWishlistedMovies()
    for w in w_movies:
        wish_movs.append(op_normalizeMovieObject(w.movie))
        
    if len(wish_movs) > 0:
        context['top_wishlist'] = wish_movs;    
    
    return render(request, 'moviediary/homepage.html', context)

def search(request):
    context = {}
    
    if request.GET.get("title"):
        context['search_title'] = request.GET.get("title")
    return render(request, 'moviediary/index.html', context)

def signup(request, username, email, password):
    #See if username exists, if so get salt add to password and hash and see if it matches hashed_password
    return HttpResponse("Attempting to sign up with username: " + username)

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

def logout_view(request):
    logout(request)
    context = {"user_status":"logged out"}
    return render(request, 'moviediary/homepage.html', context)

def change_password_view(request, username=''):
    if request.user.is_authenticated() and (username == request.user.username):
        return render(request, 'registration/changepass.html')
    else:
        return render(request, 'registration/login.html')
    
def change_password(request):
    if request.user.is_authenticated() and request.is_ajax():
        if request.POST.get('new_pass'):
            request.user.set_password(request.POST.get('new_pass'))
            return JsonResponse({"status":"success"})
        else:
            return JsonResponse({"status":"failure - no password found"})
    else:
        raise Http404
    
def remove_user_view(request, username=''):
    if request.user.is_authenticated() and (username == request.user.username):
        return render(request, 'registration/removeuser.html')
    else:
        return render(request, 'registration/login.html')
    
def remove_user(request):
    if request.user.is_authenticated() and request.is_ajax():
        request.user.delete()
        return JsonResponse({"status":"success"})
    else:
        raise Http404
    
def about_us(request):
    return render(request, 'moviediary/aboutus.html')

#TODO: Decide whether to take these out and move them to AJAX responses to reduce the 
#up front load cost of all these DB queries - okay for now but won't scale particularly well
#What's quicker - loads of DB calls up front or 3 different AJAX calls to fill in information
def profile(request, username=''):
    context = {}
    
    if (username == '') or (username == request.user.username):
        reviewer = get_object_or_404(Reviewer, user=request.user)
    else:
        try:
            user = User.objects.get(username=username)
        except:
            raise Http404
        reviewer = get_object_or_404(Reviewer, user=user)
    context['reviewer'] = reviewer
    
    wish_movs = []
    wishlists = getWishlistMoviesForReviewer(reviewer, 4)
    for w in wishlists:
        wish_movs.append(op_normalizeMovieObject(w.movie))
    
    if len(wish_movs) > 0:
        context['wishlist'] = wish_movs
    
    user_revs = []
    reviews = getReviewsForUser(reviewer)
    for r in reviews:
        user_revs.append(op_normalizeReviewObject(r))
    
    if len(user_revs) > 0:
        context['reviews'] = user_revs;
    
    context['num_following'] = getCountOfFollowersForUser(reviewer)
    
    context['num_followed'] = getCountOfFollowedsForUser(reviewer)
    
    #context['follow_reviews'] = getReviewsFromFollowed(reviewer)
    
    return render(request, 'moviediary/profile.html', context)
    
def review_form(request):
    return render(request, 'moviediary/review_form.html')

def profile_reviews(request, username='', page=1):
    context = {}
    
    if (username == '') or (username == request.user.username):
        reviewer = get_object_or_404(Reviewer, user=request.user)
    else:
        try:
            user = User.objects.get(username=username)
        except:
            raise Http404
        reviewer = get_object_or_404(Reviewer, user=user)
    
    context['reviewer'] = reviewer
    context['current_page'] = page
        
    user_revs = []
    reviews = getReviewsForUser(reviewer)
    for r in reviews:
        user_revs.append(op_normalizeReviewObject(r))
    
    p = int(page)-1
    
    if len(user_revs) > 0:
        if len(user_revs) > p*20:
            context['reviews'] = user_revs[p*20:page*20]
            context['reviews_len'] = len(user_revs)
            context['num_pages'] = (len(user_revs)/20)+1
        else:
            raise Http404
    
    return render(request, 'moviediary/profile_reviews.html', context)

def profile_wishlist(request, username='', page=1):
    context = {}
    
    if (username == '') or (username == request.user.username):
        reviewer = get_object_or_404(Reviewer, user=request.user)
    else:
        try:
            user = User.objects.get(username=username)
        except:
            raise Http404
        reviewer = get_object_or_404(Reviewer, user=user)
    
    context['reviewer'] = reviewer
    context['current_page'] = page
    
    wish_movs = []
    wishlists = getWishlistMoviesForReviewer(reviewer)
    for w in wishlists:
        wish_movs.append(op_normalizeMovieObject(w.movie))
    
    p = int(page)-1
    
    if len(wish_movs) > 0:
        if len(wish_movs) > p*20:
            context['wishlist'] = wish_movs[p*20:(page)*20]
            context['wish_length'] = len(wish_movs)
            context['num_pages'] = (len(wish_movs)/20)+1
        else:
            raise Http404
    
    return render(request, 'moviediary/profile_wishlist.html', context)

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
                
                rel_date_obj = time.strptime(review_date, "%d %B %Y")
                review_date = time.strftime("%Y-%m-%d", rel_date_obj)
                
                m = op_addMovie(movie_title,release_date,movie_id, tagline, poster_url)
                if m is 0:
                    op_removeMovieFromWishlist(m, reviewer)
                    
                r = op_addReview(reviewer, m, review_text, review_date, rating, headline)
                
                if isinstance(r, types.StringTypes):
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
                w = op_addMovieToWishlist(m,reviewer);
                if isinstance(w, types.StringTypes):
                    return JsonResponse({"wish_status":w})
                else:
                    return JsonResponse({"wish_status":"success"});
        errors['status'] = "Failed to add movie to user's wishlist";
        return JsonResponse(errors);
    else:
        return JsonResponse({"wish_status":"Not logged in"});
    
#Remove movie from wishlist for user    
def remove_movie_from_wishlist(request):
    if request.user.is_authenticated():
        errors = {}
        errors['error'] = []
        if request.method == 'POST' and request.is_ajax():
            if not request.POST.get('movie_id'):
                errors['error'].append('Invalid movie id')
            if not errors['error']:
                reviewer = get_object_or_404(Reviewer, user=request.user)
                
                m = op_getMovie(request.POST.get('movie_id'))
                if isinstance(m, types.StringTypes):
                    return JsonResponse({"wish_status":m})
                else:
                    op_removeMovieFromWishlist(m, reviewer);
                    return JsonResponse({"wish_status":"success"});
        errors['status'] = "Failed to add movie to user's wishlist";
        return JsonResponse(errors);
    else:
        return JsonResponse({"wish_status":"Not logged in"});
    
def get_movie_reviews(request, movie_id=0):
    context = {}
    
    m = get_object_or_404(Movie, ext_id=movie_id)
    
    context['movie'] = op_normalizeMovieObject(m)
    
    revs = []
    reviews = op_getReviewsForMovie(m)
    for r in reviews:
        revs.append(op_normalizeReviewObject(r))
    
    if len(revs) > 0:
        context['recent_reviews'] = revs
    
    return render(request, 'moviediary/movie_review.html', context)
    
def get_movie_info(request, movie_id=0):
    context = {}
    
    if request.is_ajax():
        m_id = request.GET.get('movie_id')
        m = op_getMovie(m_id)
        if type(m) is str:
            return JsonResponse({'status':'error - no movie found with ID'})
    else:
        m = op_getMovie(movie_id)
        if type(m) is str:
            id_obj = {'ext_id':movie_id}
            context['movie'] = id_obj
            return render(request, 'moviediary/movie_page.html', context)
            
        
    context['movie'] = op_normalizeMovieObject(m)
    context['status'] = "Success - Found movie"
    
    ctxt_revs = []
    reviews = op_getMostRecentReviewsForMovie(m)
    for r in reviews:
        ctxt_revs.append(op_normalizeReviewObject(r))
    
    if len(ctxt_revs) > 0:
        context['recent_reviews'] = ctxt_revs
    
    if request.user.is_authenticated():
        reviewer = get_object_or_404(Reviewer, user=request.user)
        r = op_getReview(m,reviewer)
        if not isinstance(r, types.StringTypes):
            context['review'] = op_normalizeReviewObject(r)
        context['wishlist'] = op_isMovieWishlisted(m,reviewer)
    
    if request.is_ajax():
        return JsonResponse(context)
    else:
        return render(request, 'moviediary/movie_page.html', context)

def edit_profile(request, username=''):
    if request.user.is_authenticated() and request.user.username==username:
        if request.method == 'POST':
            reviewer = get_object_or_404(Reviewer, user=request.user)
            
            bio = request.POST.get('bio') if request.POST.get('bio') else reviewer.bio
            love_movies = request.POST.get('love_movies') if request.POST.get('love_movies') else reviewer.love_movie_text
            fav_genres = request.POST.get('genre') if request.POST.get('genre') else reviewer.favourite_genres
            
            op_updateReviewerProfile(reviewer,bio,love_movies,fav_genres)
            
    return profile(request)
   
def get_movie_page(request, movie_id):
    context = {}
    
    m = get_object_or_404(Movie, ext_id=movie_id)
    context['movie'] = m;
    
    return render(request, 'moviediary/movie_page.html', context)

def get_movie_ratings(request):
    context = {}
    
    if request.is_ajax():
        if request.GET.get('id_list'):
            movie_ids = request.GET.get('id_list')
            movie_ids = json.loads(movie_ids)
            if len(movie_ids) > 0:
                stars = [];
                for m_id in movie_ids:
                    m = op_getMovie(m_id)
                    if isinstance(m, types.StringTypes):
                        stars.append("")
                    else:
                        stars.append(m.average_review_score)
                context['stars'] = stars
                context['status'] = 'success'
            else:
                context['status']='error'
        else:
            context['status']='error'
        return JsonResponse(context)
    else:
        return index(request);

def add_test_data(request):
    if request.user.is_authenticated() and request.is_ajax():
        op_fillTestData()
        return JsonResponse({"status":"success"})
    else :
        raise Http404
'''
Created on 2 Apr 2016

@author: Neil Donnelly
'''
import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from moviediary.db_operations import getMovieWithTMDB_Id, getUserReviewForMovie, \
    removeWishlist, getWishlistMovieForReviewer
from moviediary.models import Reviewer, Movie, Review, Wishlist, Following


#function to set up user on DB        
def op_signup(user):
    #check if username or email exist on DB already
    if user is None:
        return "User does not exist, cannot sign up"
    #create a recovery token if the user forgets their password
    recovery = uuid.uuid4().hex()
    
    #Creates user object for DB and saves
    r = Reviewer.objects.create(user=user, 
             num_of_reviews=0,
             reset_token=recovery)
    return r
    
#create a movie instance for the DB
def op_addMovie(title, release, tmdb_id, tagline, im_url):
    try:
        m = getMovieWithTMDB_Id(tmdb_id)
    except ObjectDoesNotExist:
        m = Movie.objects.create(title=title, 
                             release_date=release, 
                             ext_id=tmdb_id,
                             tagline=tagline,
                             image_url=im_url)
    return m

#get movie with id
def op_getMovie(movie_id):
    try:
        m = getMovieWithTMDB_Id(movie_id)
    except ObjectDoesNotExist:
        return "Error:Movie not in DB"
    return m

#get review for movie
def op_getReview(movie, reviewer):
    r = getUserReviewForMovie(movie, reviewer)
    if r.exists():
        return r[0]         
    else:
        return "Error:User has not reviewed " + movie.title   

#create a review for a movie from given reviewer, update reviewer and movie
def op_addReview(reviewer, movie, review_text, review_date, score, headline):
    #check if the user has already written a review for this Movie
    review = getUserReviewForMovie(movie, reviewer)
    if review.exists():
        return "Error:Failed to add review"
    else:
        #Create the new review with the updated info
        r = Review.objects.create(score=score,
                                  reviewer=reviewer,
                                  movie=movie,
                                  review_text=review_text,
                                  review_date=review_date,
                                  review_headline=headline)
        
        #Update user's number of reviews
        reviewer.num_of_reviews+=1
        reviewer.save()
        
        #Update movie's average score and number of reviews
        movie.average_review_score = ((movie.average_review_score * movie.num_of_reviews) + score)/(movie.num_of_reviews+1)
        movie.num_of_reviews+=1
        movie.save()
        
        return r;    

#add wishlist object for movie and reviewer
def op_addMovieToWishlist(movie, reviewer):
    w = Wishlist.objects.filter(reviewer=reviewer).filter(movie=movie)
    if w.exists():
        return "Error:Movie already on wishlist"
    else:
        return Wishlist.objects.create(reviewer = reviewer, movie = movie)
    
#delete the movie from the user's wishlist
def op_removeMovieFromWishlist(movie, reviewer):
    removeWishlist(reviewer, movie)
    
def op_addFollower(follower, followed):
    f = Following.objects.filter(follower=follower).filter(followed=followed)
    if f.exists():
        return "Error:User already being followed"
    else:
        return Following.objects.create(follower=follower,followed=followed)
    
def op_isMovieWishlisted(movie, reviewer):
    w = getWishlistMovieForReviewer(reviewer,movie)
    return w.exists()

#put test data into database    
def op_fillTestData():
    user_1 = User.objects.create_user(username='user_1',
                                        email='n.donnellyv3.0+user_1@gmail.com',
                                        password='user_1')
    
    r1 = Reviewer.objects.create(user=user_1, 
        num_of_reviews=0,
        reset_token="recovery")
    
    user_2 = User.objects.create_user(username='user_2',
                                        email='n.donnellyv3.0+user_2@gmail.com',
                                        password='user_2')
    
    r2 = Reviewer.objects.create(user=user_2, 
        num_of_reviews=0,
        reset_token="recovery")
    
    user_3 = User.objects.create_user(username='user_3',
                                        email='n.donnellyv3.0+user_3@gmail.com',
                                        password='user_3')
    
    r3 = Reviewer.objects.create(user=user_3, 
        num_of_reviews=0,
        reset_token="recovery")
        
    m1 = op_addMovie('Captain America: Civil War', 
                    '2016-04-27', 
                    '271110',
                    'Divided We Fall',
                    '/5N20rQURev5CNDcMjHVUZhpoCNC.jpg')
    
    m2 = op_addMovie('Hot Fuzz',
                    '2007-02-14',
                    '4638',
                    'Big cops.  Small town.  Moderate violence.',
                    '/5Jx6s6VXnunh8wCLgR0YgjwSgjh.jpg')
    
    m3 = op_addMovie('The Departed',
                    '2006-10-05',
                    '1422',
                    'Lies. Betrayal. Sacrifice. How far will you take it?',
                    '/tGLO9zw5ZtCeyyEWgbYGgsFxC6i.jpg')
    
    m4 = op_addMovie('Die Hard',
                    '1988-07-14',
                    '562',
                    '40 Stories. Twelve Terrorists. One Cop.',
                    '/mc7MubOLcIw3MDvnuQFrO9psfCa.jpg')
    
    m5 = op_addMovie('Run, Fatboy, Run',
                    '2007-09-06',
                    '7942',
                    "Love. Commitment. Responsibility. There's nothing he won't run away from.",
                    '/s6ehbUfScpU0408ahsxCzlUwAzG.jpg')
    
    op_addReview(r1, m1, "Review for user 1 and Civil War", '2016-05-04', 9, 'Really Good')
    op_addReview(r2, m1, "Review for user 2 and Civil War", '2016-05-08', 7, 'Good')
    op_addReview(r3,m2,"Review from user 3 for Hot Fuzz", '2009-09-01', 10, 'Rib-Tickling Action')
    op_addReview(r3,m1,"Review from user 3 for Civil War", '2016-05-06', 8, 'Very Good')
    op_addReview(r2,m3,"Review from user 2 for The Departed", '2007-02-14', 9, 'Thrilling')
    op_addReview(r1,m5,"Review from user 1 for Run, Fatboy, Run", '2011-08-13', 7, 'Wholesome Fun')
    
    op_addMovieToWishlist(m4, r1)
    op_addMovieToWishlist(m2, r3)
    op_addMovieToWishlist(m3, r1)
    
    op_addFollower(r3, r1)
    op_addFollower(r2, r3)
    
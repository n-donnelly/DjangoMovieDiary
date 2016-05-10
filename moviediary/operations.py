'''
Created on 2 Apr 2016

@author: Neil Donnelly
'''
import uuid

from moviediary.db_operations import getMovieWithTMDB_Id, getUserReviewForMovie
from moviediary.models import Reviewer, Movie, Review

#function to set up user on DB        
def op_signup(user):
    #check if username or email exist on DB already
    if user is None:
        return "User does not exist, cannot sign up"
    #create a recovery token if the user forgets their password
    recovery = uuid.uuid4().hex()
    
    #Creates user object for DB and saves
    r = Reviewer(user=user, 
             num_of_reviews=0,
             reset_token=recovery)
    r.save()
    return r
    
#create a movie instance for the DB
def op_addMovie(title, release, tmdb_id, tagline, im_url):
    if getMovieWithTMDB_Id(tmdb_id) is not None:
        return "movie with that ID already exists"
    m = Movie.objects.create(title=title, 
                             release_date=release, 
                             ext_id=tmdb_id,
                             tagline=tagline,
                             image_url=im_url)
    
    return m

#create a review for a movie from given reviewer, update reviewer and movie
def op_addReview(reviewer, movie, review_text, review_date, score):
    #check if the user has already written a review for this Movie
    if getUserReviewForMovie(movie, reviewer) is not None:
        return "User has already reviewed this movie"
    
    #Update user's number of reviews
    reviewer.num_of_reviews+=1
    reviewer.save()
    
    #Update movie's average score and number of reviews
    movie.average_review_score = ((movie.average_review_score * movie.num_of_reviews) + score)/(movie.num_of_reviews+1)
    movie.num_of_reviews+=1
    movie.save()
    
    #Create the new review with the updated info
    r = Review.objects.create(score=score,
                              reviwer=reviewer,
                              movie=movie,
                              review_text=review_text,
                              review_date=review_date)
    
    return r;
    
    
from moviediary.models import Movie, Review, Following, Wishlist

def getMovieWithTMDB_Id(tmdb_id):
    #SELECT * FROM Movie WHERE ext_id=tmdb_id
    return Movie.objects.get(ext_id=tmdb_id)

def getMoviesReviewedByReviewer(reviewer):
    #Should be SELECT movie FROM Review, User WHERE User.ID = Review.User,
    # testing out the reverse relations and chaining them
    return Movie.objects.filter(review__reviewer=reviewer)

def getReviewsForUser(reviewer):
    #SELECT * FROM Review WHERE UserId=reviewer.id
    return Review.objects.filter(reviewer=reviewer).order_by('-review_date')

def getReviewsForMovie(movie):
    #SELECT * FROM Review WHERE MovieId=movie.id
    return Review.objects.filter(movie=movie).order_by('-review_date')

def getUserReviewForMovie(movie, reviewer):
    #SELECT * FROM Review WHERE MovieId=movie.id AND UserId=reviewer.id
    return Review.objects.filter(movie=movie).filter(reviewer=reviewer)

def getFollowingList(reviewer):
    #SELECT * FROM Following WHERE follower=reviewer
    return Following.objects.filter(follower=reviewer)

def getFollowersList(reviewer):
    #SELECT * FROM Following WHERE follower=reviewer
    return Following.objects.filter(followed=reviewer)

def getWishlistMoviesForReviewer(reviewer, limit=0):
    #SELECT * FROM Wishlist WHERE UserId=reviewer.id
    if limit < 1:
        return Wishlist.objects.filter(reviewer=reviewer)
    else:
        return Wishlist.objects.filter(reviewer=reviewer)[:limit]

def getLatestWishlistedMovies(limit=0):
    if limit < 1:
        return Wishlist.objects.all()
    else:
        return Wishlist.objects.all()[:limit]

def getUsersWishingForMovie(movie):
    #SELECT * FROM Wishlist WHERE MovieId=movie.id
    return Wishlist.objects.filter(movie=movie)

def getLatestAddedMovies(limit):
    #SELECT * FROM Movie ORDER_BY release_date DESC
    if limit < 1:
        return Movie.objects.all().order_by('-release_date')
    return Movie.objects.all().order_by('-release_date')[:limit]

def getLatestReviews(limit):
    #SELECT * FROM Review ORDER_BY review_date DESC
    if limit < 1:
        return Review.objects.all().order_by('-review_date')
    return Review.objects.all().order_by('-review_date')[:limit]

def getReviewsFromFollowed(user):
    followeds = Following.objects.filter(follower=user).values('followed')
    return Review.objects.filter(reviewer__in=followeds).order_by('-review_date')[:5]

def getCountOfFollowersForUser(user):
    return Following.objects.filter(followed=user).count()

def getCountOfFollowedsForUser(user):
    return Following.objects.filter(follower=user).count()

def getWishlistMovieForReviewer(reviewer, movie):
    return Wishlist.objects.filter(reviewer=reviewer).filter(movie=movie)

#remove wishlist that matches reviewer and Movie
def removeWishlist(reviewer, movie):
    return Wishlist.objects.filter(reviewer=reviewer).filter(movie=movie).delete()
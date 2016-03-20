from moviediary.models import Movie, User, Review, Following, Wishlist

def getMovieWithTMDB_Id(tmdb_id):
    #SELECT * FROM Movie WHERE ext_id=tmdb_id
    return Movie.objects.get(ext_id=tmdb_id)

def getMoviesReviewedByUser(username):
    #Should be SELECT movie FROM Review, User WHERE User.ID = Review.User,
    # testing out the reverse relations and chaining them ;P
    return Movie.objects.filter(review__user__username=username)

def getUserByUsername(req_username):
    #SELECT * FROM User WHERE username=req_username
    return User.objects.get(username = req_username)

def getReviewsForUser(req_user):
    #SELECT * FROM Review WHERE UserId=req_user.id
    return Review.objects.filter(user=req_user)

def getReviewsForMovie(req_movie):
    #SELECT * FROM Review WHERE MovieId=req_movie.id
    return Review.objects.filter(movie=req_movie)

def getFollowingList(req_user):
    #SELECT * FROM Following WHERE follower=req_user
    return Following.objects.filter(follower=req_user)

def getFollowersList(req_user):
    #SELECT * FROM Following WHERE follower=req_user
    return Following.objects.filter(followed=req_user)

def getWishlistMovies(req_user):
    #SELECT * FROM Wishlist WHERE UserId=req_user.id
    return Wishlist.objects.filter(user=req_user)

def getUsersWishingForMovie(req_movie):
    #SELECT * FROM Wishlist WHERE MovieId=req_movie.id
    return Wishlist.objects.filter(movie=req_movie)
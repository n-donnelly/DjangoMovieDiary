$(document).ready(function(){
	
	loadStarsDiv()
	
	retrieveTMDBUpcomingMovies(function(data){
		fillUpcomingDiv(data);
	});
	retrieveTMDBPlayingMovies(function(data){
		fillPlayingDiv(data);
	})
})

function retrieveTMDBUpcomingMovies(callback) {
	tmdb.call('/movie/upcoming',
			{},
			callback,
			function(data){
				console.log(data)
			})
}

function retrieveTMDBPlayingMovies(callback) {
	tmdb.call('/movie/now_playing',
			{},
			callback,
			function(data){
				console.log(data)
			})
}

function getStarsForMovieDiv(data,div) {
	$.ajax({
		type:'GET',
		url:'/moviediary/get_movie_ratings/',
		dataType:"json",
		data:{
			'id_list':JSON.stringify(data)
		},
		success: function (data) {
			if(data['status'].startsWith("error"))
				console.log("Movie not on the DB with id " + movie['id']);
			else {
				var stars = $(div).find(".rev_stars");
				for(var i = 0; i < 8; i++){
					if(data['stars'][i]!="" && data['stars'][i]!=0){
						$(stars).eq(i).html(data['stars'][i]);
						loadStarsForOneDiv($(stars).eq(i));
					}
				}
			}
		}
	})
}

function fillUpcomingDiv(data){
	var latest_str = "";
	var movie_id_arr = [];
	for(i = 0; i < 8; i++){
		movie = data.results[i];
		movie_id_arr.push(movie.id);
		latest_str += createTMDBDiv(movie);
	}
	var id_list = {"id_list":movie_id_arr};
	$("#upcoming_releases_roll").append(latest_str);
	getStarsForMovieDiv(movie_id_arr,$("#upcoming_releases_roll"));
}

function fillPlayingDiv(data){
	var latest_str = "";
	var movie_id_arr = [];
	for(i = 0; i < 8; i++){
		movie = data.results[i];
		movie_id_arr.push(movie.id);
		latest_str += createTMDBDiv(movie);
	}
	var id_list = {"id_list":movie_id_arr};
	$("#latest_releases_roll").append(latest_str);
	getStarsForMovieDiv(movie_id_arr,$("#latest_releases_roll"));
}

function createTMDBDiv(movie){
	mStr = "<div class='movie_div'>";
	if(movie.poster_path != null){
		mStr += "<div class='movie_image smaller_image'><a href='/moviediary/movie/" + movie.id + "/'>";
		mStr += "<img src='http://image.tmdb.org/t/p/w500" + movie.poster_path + "'></a></div>"
	}
	mStr += "<div class='rev_details'><a class='movie_title' href='/moviediary/movie/" + movie.id + "/'>" + movie.title + "</a>";
	mStr += "<span class='movie_release'>" + getDateString(new Date(movie.release_date)) + "</span>";
	mStr += "<div class='rev_stars'></div>";
	mStr += "</div></div>";
	return mStr;
}
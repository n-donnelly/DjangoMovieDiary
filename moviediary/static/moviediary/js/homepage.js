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

function fillUpcomingDiv(data){
	var latest_str = "";
	for(i = 0; i < 8; i++){
		movie = data.results[i];
		latest_str += "<span>" + movie.title + "</span>";
	}
	$("#upcoming_releases_roll").append(latest_str);
}

function fillPlayingDiv(data){
	var latest_str = "";
	for(i = 0; i < 8; i++){
		movie = data.results[i];
		latest_str += "<span>" + movie.title + "</span>";
	}
	$("#latest_releases_roll").append(latest_str);
}
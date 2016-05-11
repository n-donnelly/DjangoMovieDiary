var current_movie_list;
var monthNames = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"];
var rtn_tom_page_limit = "page_limit=";
var pg_limit = 10;
var query = "";
var is_user_auth = "{{% user.is_authenticated %}}"

$("#title_search_btn").on("click", searchMovieTitle);

$('#title_search_txt').keydown(function(event){
	if ( event.which == 13 ) {
	   event.preventDefault();
	   searchMovieTitle();
	}
})

function loadResults(data){
	createResultsString(data, function(results){
		$("#movies_list").append(results);
		$(".review_btn").on("click", function(event){
			//$(event.target).parent().load("review_form")
			$.get("review_form", function(data) {
				$(data).appendTo($(event.target).parent());
				$("#datepicker").datepicker();
				//$("#datepicker").datepicker("option", "showAnim", "slideDown");
			})
		})
	});
}

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function createResultsString(data, finished_callback) {
	var testQuery = query;
	current_movie_list = data.results;
	var results_str = "";
	$.each(current_movie_list, function(index, movie){
		var mStr = buildItem(movie, index);
		results_str += mStr;
	})	
	finished_callback(results_str)
}

function expandMovie(obj) {
	var movie_index = obj['selector'].substring(7);
	var movie = current_movie_list[movie_index];
	
	tmdb.call('/movie/' + movie['id'],{},function(data) {
		var detailsDiv = obj.children(".movie_deets");
		detailsDiv.append(buildExtraDetailsString(data));
	})
}

function buildExtraDetailsString(movie) {
	extraStr = "<div id='extras'>";
	
	extraStr += "</div>";
	return extraStr;
}

function searchMovieTitle() {
	q=$("#title_search_txt").val();					
	$("#movies_list").empty();
	tmdb.call('/search/movie', 
			{
				"query":q,
				include_adult: true
			},
			loadResults)
}

function buildItem(movie, index) {
	
	var builtStr = "<li id='movie_" + index + "'><div><div class='movie_image'>";
	builtStr += getImageUrl(movie);
	builtStr += "</div><div class='movie_deets'>";
	var arr = {'Title' : movie.title,
			'Year' : getDateString(new Date(movie.release_date)),
			'Overview' : movie.overview}
	builtStr += buildString(arr) + '</div>';
	
	if (is_user_auth) {
		builtStr += "<a class='review_btn'>Review this Movie</a>";
	} 
	
	builtStr += "</div></li>"
	return builtStr;
}

function getImageUrl(movie) {
	if (movie['poster_path'] == null){
		return "";
	}
	var imUrl = tmdb.images_uri+'/w500'+movie['poster_path'];
	return '<img src="' + imUrl + '"/>';
}

function buildString (elemArr) {
	var startItem = '<span>';
	var endItem = '</span>';
	var midItem = '</span><span>';
	
	var retStr = startItem;
	var i = 0;
	for(var elem in elemArr) {
		if(elemArr.hasOwnProperty(elem)){
			if(elemArr[elem] != "-1%" && elemArr[elem] != "" && elemArr[elem] != "null"){
				retStr += elemArr[elem];
				retStr += (i == Object.size(elemArr) - 1 ? endItem : midItem);
			}
			i++;
		}
	}
	
	return retStr;
}

function getDateString(date) {
	var dateString = date.getUTCDate() + ' ';
	dateString += monthNames[date.getUTCMonth()] + ' ';
	dateString += date.getUTCFullYear();
	return dateString;
}
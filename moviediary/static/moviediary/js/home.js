var lang = navigator.languages? navigator.languages[0] : (navigator.language || navigator.userLanguage);

var rtn_tom_page_limit = "page_limit=";
var pg_limit = 10;
var query = "";

var apikey = "gurega4bpq42fnt9asvb5adv";
var baseUrl = "http://api.rottentomatoes.com/api/public/v1.0";
var moviesSearchUrl = baseUrl + '/movies.json?apikey=' + apikey;
var moviesInfoUrl = baseUrl + "/movies/";
var jsonStr = ".json?apikey=";
var q = "";
	
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
	});
}

Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};
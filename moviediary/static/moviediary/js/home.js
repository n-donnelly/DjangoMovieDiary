var lang = navigator.languages? navigator.languages[0] : (navigator.language || navigator.userLanguage);

$("#title_search_btn").on("click", trySearch);

$('#title_search_txt').keydown(function(event){
	if ( event.which == 13 ) {
	   event.preventDefault();
	   trySearch();
	}
})

function trySearch(){
	if($("#movies_list").length)
		searchMovieTitle();
	else
		$("#searchbar").submit();
}
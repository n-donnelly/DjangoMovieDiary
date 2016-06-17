var lang = navigator.languages? navigator.languages[0] : (navigator.language || navigator.userLanguage);

$("#title_search_btn").on("click", trySearch);

$('#title_search_txt').keydown(function(event){
	if ( event.which == 13 ) {
	   event.preventDefault();
	   trySearch();
	}
})

function trySearch(){
	$("#searchbar").submit();
}

function loadStarsDiv(){
	$(".rev_stars").each(function(i){
		loadStarsForOneDiv(this)
	})
}

function loadStarsForOneDiv(starDiv) {
	var score = $(starDiv).html();
	revStr = "";
	score = Math.round(parseFloat(score));
	for(var i = 0; i < (score-1)/2; i++){
		revStr += "<span class='star'></span>";
	}
	if (parseInt(score)%2!=0) {
		revStr += "<span class='star half'></span>";
	}
	$(starDiv).html(revStr);
}
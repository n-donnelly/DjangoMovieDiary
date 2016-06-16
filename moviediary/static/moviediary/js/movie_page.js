$(document).ready(function(){
	
	loadStarsDiv()
	
	retrieveTMDBMovie(movie_id, function(data){
		loadTMDBExtrasDiv($(".tmdb_extras"), data, true);
	})
})

function onSubmitClicked(event){
	$(event.target).submit();
}

function submitFormAJAX(event) {
	var form = $(event.target).parent();
	//console.log("Submit object: " + thisObj);
	var ajax_data = form.serializeArray();
	$.ajax({
		type:'POST',
		url:'/moviediary/review_submit/',
		data:form.serializeArray(),
		success: function (data) {
			form.html(data['review_status']);
			location.reload();
		},
		error: function(request, status, error) {
			console.log("Something went wrong: " + request.responseText)
		}
	})
}

function fillHiddenForm(target, form) {
	form.find("#movie_title").val(movie_title);
	form.find("#movie_id").val(movie_id);
	form.find("#poster_url").val(movie_poster_url);
	form.find("#release_date").val(movie_release);
}
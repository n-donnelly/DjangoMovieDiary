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
		},
		error: function(request, status, error) {
			console.log("Something went wrong: " + request.responseText)
		}
	})
}

function fillHiddenForm(target, form) {
	var movie_id = $(target).offsetParent().attr('id').split('_')[1];
	
	form.find("#movie_title").val(current_movie_list[movie_id].title);
	form.find("#movie_id").val(current_movie_list[movie_id].id);
	form.find("#poster_url").val(current_movie_list[movie_id].poster_path);
	form.find("#release_date").val(current_movie_list[movie_id].release_date);
}
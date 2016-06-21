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
			movie_li = $(form).offsetParent();
			var movie_index = movie_li.attr("id").split("_")[1];
			var movie = current_movie_list[movie_index];
			$(movie_li).find(".extra_deets").remove();
			$(movie_li).find(".mebert_extras").remove();
			buildExtraDivs(movie_li);
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
	form.find("#tagline").val(current_movie_list[movie_id].tagline);
}
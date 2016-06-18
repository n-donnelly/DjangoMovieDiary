$(document).ready(function(){
	
	loadStarsDiv()
	
	retrieveTMDBMovie(movie_id, function(data){
		loadTMDBExtrasDiv($(".tmdb_extras"), data, true);
		
		if(movie_title == ""){
			$("#title").html(data.title);
			$("#release").html(data.release_date);
			$(".movie_image img").attr("src", $(".movie_image img").attr("src")+data.poster_path)
			movie_title = data.title;
			movie_release = data.release_date;
			movie_poster_url = data.poster_path;
			taglin = data.tagline;
		}
		
		$(".wish_btn").off("click");
		$(".not_wished").on("click",function(event){
			wishlistArr = {};
			wishlistArr['csrfmiddlewaretoken'] = Cookies.get('csrftoken');
			wishlistArr['tagline'] = tagline;
			wishlistArr['movie_title'] = movie_title;
			wishlistArr['release_date'] = movie_release;
			wishlistArr['movie_id'] = movie_id;
			wishlistArr['poster_url'] = movie_poster_url;
			
			requestWishlist($(event.target),wishlistArr);
		});
		$(".wished").on("click", function(event){
			requestRemoveFromWishlist($(event.target),movie_id);
		})
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
	form.find("#tagline").val(tagline);
}
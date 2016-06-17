var current_movie_list;
var monthNames = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"];
var rtn_tom_page_limit = "page_limit=";
var pg_limit = 20;
var query = "";
var is_user_auth = "{{% user.is_authenticated %}}";

$(document).ready(function(){
	if(typeof init_query !== 'undefined') {
		$("#title_search_txt").val(init_query);
		searchMovieTitle();
	}
})

function retrieveTMDBMovie(id, callback) {
	tmdb.call('/movie/' + id,
		{
			"append_to_response":"credits"
		},
		callback)
}
	
function loadResults(data){
	createResultsString(data, function(results){
		$("#movies_list").append(results);
		$(".movie_image").on("click", expandMovie);
		$(".movie_deets").on("click", expandMovie);
	});
}

function loadForm(event) {
	$.get("/moviediary/review_form", function(data) {
		$(event.target).html("Nevermind");
		$(event.target).off("click");
		$(event.target).on("click", hideForm);
		$(event.target).parent().find(".movie_form").remove();
		$(data).appendTo($(event.target).parent());

		var form = $(event.target).parent().find(".movie_form");
		form.submit(submitFormAJAX);
		form.find("#form_btn").on("click", onSubmitClicked);
		//Forcing the use of the Irish locale for the datepicker so the server can parse the date string
		//Needs to be fixed so the locale can be changed per user and the client sends the right format so the server doesn't need to parse
		$("#datepicker").datepicker({"dateFormat":"dd MM yy"});
		
		fillHiddenForm(event.target, form);
		
		//$(event.target).parent().find(".movie_form").hide().slideDown(1000);
	})
	
}

function hideForm(event) {
	var form = $(event.target).parent().find(".movie_form");
	form.remove();
	$(event.target).off("click");
	$(event.target).on("click", loadForm);
	$(event.target).html("Review this Movie");
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

function expandMovie(event) {
	var movie_li = $(event.target).offsetParent();
	var movie_index = movie_li.attr("id").split("_")[1];
	var movie = current_movie_list[movie_index];
	
	if(movie_li.find(".extra_deets").length)
		movie_li.find(".extra_deets").show("slow");
	else {
		extraStr = "<div class='extra_deets'><div class='tmdb_extras'></div><div class='mebert_extras'></div>";
		if (is_user_auth) {
			extraStr += "<a class='review_btn movie_action_btn'>Review this Movie</a>";
			extraStr += "<a class='wish_btn movie_action_btn'>Add to Wishlist</a>";
		}
		extraStr += "</div>";
		movie_li.children(":first").append(extraStr);
		$.ajax({
			type:'GET',
			url:'/moviediary/get_movie_info/',
			dataType:"json",
			data:{
				"movie_id":movie['id']
			},
			success: function (data) {
				if(data['status'].startsWith("error"))
					console.log("Movie not on the DB with id " + movie['id']);
				else
					if(data.review) {
						movie_li.children(":first").find(".review_btn").hide();
						movie_li.children(":first").find(".wish_btn").hide();
					}
					if(data.wishlist) {
						movie_li.children(":first").find(".wish_btn").hide();
					}
					movie_li.children(":first").find(".mebert_extras").append(buildMebertsExtraString(data));
					
					var m_title = movie_li.find("#title").html();
					var newTitleStr = "<a href='/moviediary/movie/"+movie['id']+"/'>" + m_title + "</a>";
					movie_li.find("#title").html(newTitleStr);

					loadStarsForOneDiv(movie_li.children(":first").find(".mebert_extras").find("#ave_star"));
			}
		})
		
		
		retrieveTMDBMovie(movie['id'], function(data){
			loadTMDBExtrasDiv(movie_li.children(":first").find(".tmdb_extras"), data, false)
		})
	}
	
	movie_li.find(".movie_image").off("click");
	movie_li.find(".movie_deets").off("click");
	movie_li.find(".movie_image").on("click", hideMovieExtras);
	movie_li.find(".movie_deets").on("click", hideMovieExtras);
}

function loadTMDBExtrasDiv(tmdbDiv, data, full_details) {
	$(tmdbDiv).append(buildExtraDetailsString(data, full_details));
	$(tmdbDiv).parent().find(".review_btn").on("click", loadForm);
	$(tmdbDiv).parent().find(".wish_btn").on("click", addToWishlist);
}

function hideMovieExtras(event) {
	var movie_li = $(event.target).offsetParent();
	movie_li.find(".extra_deets").hide("slow");
	
	movie_li.find(".movie_image").off("click");
	movie_li.find(".movie_deets").off("click");
	movie_li.find(".movie_image").on("click", expandMovie);
	movie_li.find(".movie_deets").on("click", expandMovie);
}

function buildMebertsExtraString(info) {
	var mebertStr = "";
	var arr = {
			'Number of Reviews':info.movie.num_of_reviews
	}
	mebertStr += buildExtrasString(arr);
	
	mebertStr += "<div class='extras_div'><span class='extras_label'>Average Score:</span><div class='rev_stars' id='ave_star'>" + info.movie.average_review_score + "</div>";
	
	if(info.review) {
		mebertStr += "<div class='extras_div'>" + buildReviewDiv(info.review, true) + "</div>";
	} 
	else if(info.recent_reviews){
		mebertStr += "<div class='extras_div'><span class='rec_rev_label'>Latest Reviews</span>";
		for(r in info.recent_reviews){
			mebertStr += buildReviewDiv(info.recent_reviews[r], false);
		}
		mebertStr += "</div>"
	}
	return mebertStr;
}

function buildReviewDiv(rev, user_review) {
	var revStr = "<div class='review_view'>";
	
	//If the review is from the user, the username will just say Your Review
	if (user_review) {
		revStr += "<span class='rev_username'>Your Review</span>";
	} else {
		//Otherwise, print user's name and make it a link for the profile of the user
		revStr += "<a class='rev_username' href='profile/"+rev.reviewer+"/'>" + rev.reviewer + "</a>";
	}
	
	//Add the review score
	revStr += "<div class='rev_stars'>";
	for(var i = 0; i < ((parseInt(rev.score)-1)/2); i++){
		revStr += "<span class='star'></span>";
	}
	if (parseInt(rev.score)%2!=0) {
		revStr += "<span class='star half'></span>";
	}
	revStr += "</div>";
	
	//Add the review date
	revStr += "<span class='rev_date'>" + getDateString(new Date(rev.review_date)) + "</span>";
	
	//Add the review headline
	revStr += "<span class='rev_headline'>" + rev.review_headline + "</span>";
	
	//Add the review text
	revStr += "<p class='rev_text'>" + rev.review_text + "</span>";
	
	revStr += '</div>';
	
	return revStr;
}

function buildExtraDetailsString(movie, full_details) {
	extraStr = "";
	
	var arr = {
			'Tagline':movie.tagline,
			'Runtime':movie.runtime,
			'Genres':buildStringFromArr(movie.genres),
			'TMDB Vote':movie.vote_average
	}
	
	if (full_details) {
		arr['Directors'] = buildDirectorString(movie.credits.crew);
		arr['Writers'] = buildWritersString(movie.credits.crew);
		arr['Cast'] = buildCastString(movie.credits.cast);
		arr['Production'] = buildStringFromArr(movie.production_companies);
	}
	
	extraStr += buildExtrasString(arr)
	
	return extraStr;
}

function buildCastString(cast){
	var castString = "";
	for(var i = 0; i < cast.length && i < 5; i++) {
		castString += "<div class='cast_member'>";
		castString += "<div class='actor'>" + cast[i].name + "</div>";
		var charStr = cast[i].character.replace("/", "</span><span>")
		castString += "<div class='character'><span>" + charStr + "</span></div>";
		castString += "<hr>";
		castString += "</div>"
	}
	return castString;
}

function buildDirectorString(crew){
	var crewString = "";
	for(var obj in crew) {
		if(crew[obj].job == "Director")
			crewString += crew[obj].name + ", ";
	}
	return crewString.substring(0, crewString.length-2);
}

function buildWritersString(crew){
	var crewString = "";
	for(var obj in crew) {
		if(crew[obj].job == "Screenplay")
			crewString += crew[obj].name + ", ";
	}
	return crewString.substring(0, crewString.length-2);
}

function buildStringFromArr(array){
	var retString = "";
	for(var obj in array){
		retString += array[obj].name + ", ";
	}
	return retString.substring(0, retString.length-2);
}

function searchMovieTitle() {
	q=$("#title_search_txt").val();					
	$("#movies_list").empty();
	tmdb.call('/search/movie', 
			{
				"query":q,
				include_adult: false
			},
			loadResults)
}

function addToWishlist(event) {
	var movie_id = $(event.target).parent().parent().parent().attr('id').split('_')[1];
	
	var wishlistArr = {};
	
	//Get the tagline from the span
	var tagline = "";
	var tagDiv = $(event.target).parent().find(".tmdb_extras .extras_div")[0];
	var tagLabel = $(tagDiv).find(".extras_label");
	if ($(tagLabel).html().startsWith("Tagline")) {
		var tagSpan = $(tagDiv).find(".extras_val");
		tagline = $(tagSpan).html();
	}
	
	var title = current_movie_list[movie_id].title;
	var release = current_movie_list[movie_id].release_date;
	var mov_id = current_movie_list[movie_id].id;
	var img_url = current_movie_list[movie_id].poster_path;
	
	wishlistArr['csrfmiddlewaretoken'] = Cookies.get('csrftoken');
	wishlistArr['tagline'] = tagline;
	wishlistArr['movie_title'] = title;
	wishlistArr['release_date'] = release;
	wishlistArr['movie_id'] = mov_id;
	wishlistArr['poster_url'] = img_url;
	
	$.ajax({
		type:'POST',
		url:'/moviediary/add_movie_to_wishlist/',
		data:wishlistArr,
		success:function(data) {
			$(event.target).html(data['wish_status']);
		},
		error: function(request, status, error) {
			console.log("Something went wrong: " + request.responseText)
		}
	})
}

function buildItem(movie, index) {
	
	var builtStr = "<li id='movie_" + index + "'><div class='movie_info'><div class='movie_image'>";
	builtStr += getImageUrl(movie);
	builtStr += "</div><div class='movie_deets'>";
	builtStr += "<a id='title' href='/moviediary/movie/"+movie.id+"/'>"+movie.title+"</a>";
	var arr = {'release' : getDateString(new Date(movie.release_date)),
			'overview' : movie.overview}
	builtStr += buildString(arr) + '</div>';
	
	/*if (is_user_auth) {
		builtStr += "<a class='review_btn'>Review this Movie</a>";
	} */
	
	builtStr += "</div></li>"
	return builtStr;
}

function getImageUrl(movie) {
	if (movie['poster_path'] == null){
		return '<img src="/static/moviediary/images/no_image.jpg"/>';
	}
	var imUrl = tmdb.images_uri+'/w500'+movie['poster_path'];
	return '<img src="' + imUrl + '"/>';
}

function buildString (elemArr) {	
	var retStr = "";
	for(var elem in elemArr) {
		if(elemArr.hasOwnProperty(elem)){
			retStr += "<span id='" + elem + "'>" + elemArr[elem] + "</span>"
		}
	}
	
	return retStr;
}

function buildExtrasString (arr) {
	var itemStart = "<div class='extras_div'><div class='extras_label'>";
	var itemMid = "</div><div class='extras_val'>";
	var itemEnd = "</div></div>";
	
	var retStr = "";
	for (var lab in arr) {
		if(arr.hasOwnProperty(lab)){
			if(arr[lab] != "-1%" && arr[lab] != "" && arr[lab] != "null"){
				retStr += itemStart + lab + ": " + itemMid + arr[lab] + itemEnd;
			}
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
var months = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July',
                   'August', 'September', 'October', 'November', 'December'];
var days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];

$(document).ready(new function(){
	refreshPage();
})

function refreshPage(){
updateCalHeader();
	
	buildCalendar();
	fillCalendar();
	
	$("#prev_month").on("click", gotoPrevMonth);
	$("#next_month").on("click", gotoNextMonth);
}

function updateCalHeader() {
	var header_compnts = $("#month_year_header").html().split(" ");
	$("#month_year_header").html(months[parseInt(header_compnts[0])-1] + " " + header_compnts[1]);
}

function buildCalendar(){
	var firstDate = new Date(year, month-1,1);
	var numDaysForMonth = new Date(year, month, 0).getDate();
	
	var cur_week = 1;
	var day_i = firstDate.getDay() < 1 ? 7 : firstDate.getDay();
	for(var date_i = 1; date_i <= numDaysForMonth;date_i++){
		var calDay = $("#week_" + cur_week + " #d_" + day_i);
		$(calDay).addClass("included");
		fillTDDiv($(calDay).children()[0], new Date(year, month, date_i));
		
		if (day_i == 7){
			day_i = 1;
			cur_week++;
		} else {
			day_i++;
		}
	}
	
	if (cur_week < 6) {
		$("#week_6").hide();
	} else {
		$("#week_6").hide();
	}
	
}

function fillCalendar(){
	if (reviewed_movies){
		var rev_movs = JSON.parse(reviewed_movies);

		for(var i = 0; i < rev_movs.length; i++) {
			var rev_date = new Date(rev_movs[i].review_date);
			addRevMovie($("#day_"+rev_date.getDate()), rev_movs[i]);
		}
	}
	
	if (wishlist_movies) {
		var wish_movs = JSON.parse(wishlist_movies);
		
		for(var i = 0; i < wish_movs.length; i++) {
			var rel_date = new Date(wish_movs[i].release_date);
			addWishMovie($("#day_"+rel_date.getDate()), wish_movs[i]);
		}
	}
	
	loadStarsDiv();
}

function fillTDDiv(dayDiv, date){
	$(dayDiv).find(".day_num").html(date.getDate());
	$(dayDiv).find(".day_content").attr("id", "day_" + date.getDate());
}

function addRevMovie(div,rev){
	var clone = $("#hidden_wrapper .movie_content").clone();
	
	$(clone).find(".movie_title").html(rev.movie.title);
	var href = $(clone).attr("href");
	$(clone).attr("href", href + rev.movie.ext_id + "/");
	
	$(clone).find(".rev_stars").html(rev.score);
	
	$(clone).addClass("review_content");
	
	$(clone).appendTo($(div));
}

function addWishMovie(div,movie){
	var clone = $("#hidden_wrapper .movie_content").clone();
	
	$(clone).find(".movie_title").html(movie.title);
	var href = $(clone).attr("href");
	$(clone).attr("href", href + movie.ext_id + "/");
	
	if(movie.average_review_score == 0)
		$(clone).find(".rev_stars").remove();
	
	$(clone).addClass("wish_content");
	
	$(clone).appendTo($(div));
}

function gotoPrevMonth(event){
	var new_month = month == 0 ? 12 : month-1;
	var new_year = month==12 ? year-1 : year;
	
	refreshCalendar(new_month,new_year);
	
	$(".angle_month").off("click");
}

function gotoNextMonth(event){
	var new_month = month == 12 ? 1 : month+1;
	var new_year = month == 1 ? year+1 : year;
	
	refreshCalendar(new_month,new_year);
	
	$(".angle_month").off("click");
}

function refreshCalendar(new_month,new_year){
	dataArr = {};
	dataArr['month'] = new_month;
	dataArr['year'] = new_year;
	$.ajax({
		type:'GET',
		url:$(location).attr("href"),
		data:dataArr,
		success:function(data) {
			month = new_month;
			year = new_year;
			reviewed_movies = data.reviewed_movies;
			wishlist_movies = data.wishlist_movies;
			
			$("td").removeClass("included");
			$(".day_num").html("");
			$(".day_content").html("");
			
			$("#month_year_header").html(month + " " + year);
			refreshPage();			
		},
		error:function(request,status,error) {
			
		}
	})
}
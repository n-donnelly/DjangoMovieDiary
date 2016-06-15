$(document).ready(function(){
	$(".rev_stars").each(function(i){
		var score = $(this).html();
		revStr = "";
		score = Math.round(parseFloat(score));
		for(var i = 0; i < (score-1)/2; i++){
			revStr += "<span class='star'></span>";
		}
		if (parseInt(score)%2!=0) {
			revStr += "<span class='star half'></span>";
		}
		$(this).html(revStr);
	})
})

$('#test_data_btn').on('click', function(event){
	$.ajax({
		type:'GET',
		url:'/moviediary/add_test_data/',
		success:function(data) {
			$(event.target).html('D');
		},
		error: function(request,status,error) {
			console.log("Something went wrong: " + request.responseText)
		}
	})
})

$('#bio_btn').on('click', showProfileForm)

function showProfileForm(event){
	$("#profile_form").show();
	$("#bio_btn").off('click');
	$("#bio_btn").on('click', hideProfileForm)
	$("#bio_btn").html('Nevermind');
}

function hideProfileForm(event){
	$("#profile_form").hide();
	$("#bio_btn").off('click');
	$("#bio_btn").on('click', showProfileForm)
	$("#bio_btn").html('Edit Your Profile');
}
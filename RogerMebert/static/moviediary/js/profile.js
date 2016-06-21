$(document).ready(function(){
	loadStarsDiv();
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
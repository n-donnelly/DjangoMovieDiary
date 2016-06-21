$("#register").submit(function(event){
	var form = $(this);
	event.preventDefault();
	$.ajax({
		type:'POST',
		url:'/moviediary/accounts/register/',
		data:form.serializeArray(),
		success: function (data) {
			if (data.status == "success"){
				$("#login #username").val($("#register #username").val());
				$("#login #password").val($("#register #password").val());
				$("#login").submit();
			} else {
				$(".error").html(data.reason);
				$("#pass_input").val("");
			}
		},
		error: function(request, status, error) {
			console.log("Something went wrong: " + request.responseText)
		}
	})
})

$("#remove_form").submit(function(event){
	var form = $(this);
	var rem_url = $(location).attr("href");
	var new_url = rem_url.substring(0,rem_url.length-6)+'/';
	event.preventDefault();
	$.ajax({
		type:'POST',
		url:new_url,
		data:form.serializeArray(),
		success: function (data) {
			if (data.status == "success"){
				$(location).attr("href", "/moviediary/")
			} else {
				$(".error").html(data.reason);
			}
		},
		error: function(request, status, error) {
			console.log("Something went wrong: " + request.responseText)
		}
	})
})
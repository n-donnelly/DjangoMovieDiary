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
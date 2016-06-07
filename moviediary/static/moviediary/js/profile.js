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
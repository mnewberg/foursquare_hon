$(document).ready(function() {

	$('#venue, #tel').on('focus', function(){
		$(this).next().html('');
	});
	
	$('#venue').on('blur', function(){
		if($(this).val() == ''){
			$(this).next().html('Venue name');
		}
	});

	$('#tel').on('blur', function(){
		if($(this).val() == ''){
			$(this).next().html('555-555-5555');
		}
	});
});
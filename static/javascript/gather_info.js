$(document).ready(function() {

	

	 jQuery.validator.addMethod("phoneUS", function(phone_number, element) {
    phone_number = phone_number.replace(/\s+/g, ""); 
	return this.optional(element) || phone_number.length > 9 &&
		phone_number.match(/^(1-?)?(\([2-9]\d{2}\)|[2-9]\d{2})-?[2-9]\d{2}-?\d{4}$/);
}, "Please specify a valid phone number");

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

	$("#gather_info_form").validate({
		  rules: {
		    twitter: {
		      required: true,
		    },
		    tel: {
		      required: true,
		      phoneUS: true
		    },
		    venue: {
		      required: true,
		    }
		  },

		  errorPlacement: function(error, element) {
		        error.insertBefore($(element).parent());
		    }
		});
	$('#button').on('click', function(){

		
		var validated=$("#gather_info_form").valid();
	    if (validated){
	    	submit();
	    }

	});
	
});

$(document).bind('DOMNodeInserted',function(){
  	$('.ui-menu').appendTo('#venue-dropdown');
});
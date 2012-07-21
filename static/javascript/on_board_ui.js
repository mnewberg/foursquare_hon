$(document).ready(function() {

	$('#arrow').on('click', function(){
		$('#screens').animate({
	    	marginLeft: '-320px'
	    });
	});

	$('#back_arrow').on('click', function(){
		$('#screens').animate({
	    	marginLeft: '0px'
	    });
	});


});
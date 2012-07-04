$(document).ready(function() {

	$('#logo').on('click', function(){
		waiting_room_to_game();
	});

	$('#game_input').on('focus', function(){
		$('#helper_text').html('');
		window.scrollTo(0, 0);
	});
	$('#game_input').on('blur', function(){
		if($('#game_input').val() == ''){
			$('#helper_text').html('Guess a '+noun);
		}
	});

	$('#clear').on('click', function(){
		$('#game_input').val('');
		$('#game_input').focus();
		window.scrollTo(0, 0);
	});


	//GAME HINT CAROUSEL ============= {

	    //move the last list item before the first item so that the user can click forward or back
	    $('#carousel_ul li:first').before($('#carousel_ul li:last'));

	    //right arrow click
	    $('.right_arrow img').click(function(){
	        //get the width of the items
	        	var item_width = $('#carousel_ul li').outerWidth();

	        //calculate the new left indent of the unordered list
	        	var left_indent = parseInt($('#carousel_ul').css('left')) - item_width;

	        //make the sliding effect using jquery's anumate function '
	            $('#carousel_ul').animate({
	            	'left' : left_indent
	            }, 500, function(){
	                //get the first list item and put it after the last list item
	                	$('#carousel_ul li:last').after($('#carousel_ul li:first'));

	                //set left indent
	                	$('#carousel_ul').css({'left' : '-204px'});
	            });
	    });

	    //left arrow click
	    $('.left_arrow img').click(function(){
	    	//get the width of the items
	        	var item_width = $('#carousel_ul li').outerWidth();

	        //calculate the new left indent of the unordered list
	        	var left_indent = parseInt($('#carousel_ul').css('left')) + item_width;

	        $('#carousel_ul').animate({
	        	'left' : left_indent
	        }, 500, function(){
	            //get the first list item and put it after the last list item
	            	$('#carousel_ul li:first').before($('#carousel_ul li:last'));

	            //set left indent
	            	$('#carousel_ul').css({'left' : '-204px'});
	        });
	    });

	//GAME HINT CAROUSEL ============= }

});

function game_over(){
	$('#lightbox').css('display', 'table');
	$('#lightbox').animate({
    	opacity: 1
    });
}

function waiting_room_to_game(){
	$('#game').animate({
    	opacity: 1
    });
    //$('#game').css('height','auto');
	$('#waiting_room').slideUp('slow', function() {
	    // Animation complete.
	});
}
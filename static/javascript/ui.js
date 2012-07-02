$(document).ready(function() {

	$('#logo').on('click', function(){
		waiting_room_to_game();
	});

	$('#game_input').on('focus', function(){
		$('#helper_text').html('');
	});
	$('#game_input').on('blur', function(){
		if($('#game_input').val() == ''){
			$('#helper_text').html('Guess a '+noun);
		}
	});

	$('#game_input').on('focus', function(){
		window.scrollTo(0, 0);
	}

	$('#clear').on('click', function(){
		$('#game_input').val('');
		$('#game_input').focus();
		//window.scrollTo(0, 0);
	});

});

function waiting_room_to_game(){
	$('#game').animate({
    	opacity: 1
    });
	$('#waiting_room').slideUp('slow', function() {
	    // Animation complete.
	});
}
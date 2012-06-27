$(document).ready(function() {

	$('#logo').on('click', function(){
		waiting_room_to_game();
	});

	$('#game_input').on('focus', function(){
		$('#helper_text').html('');
	});
	$('#game_input').on('blur', function(){
		if($('#game_input').val() == ''){
			$('#helper_text').html('Make a guess');
		}
	});

	$('#clear').on('click', function(){
		$('#game_input').val('');
		$('#game_input').focus();
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
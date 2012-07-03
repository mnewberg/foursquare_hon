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

});

function waiting_room_to_game(){
	$('#game').animate({
    	opacity: 1
    });
    $('#game').css('height','auto');
	$('#waiting_room').slideUp('slow', function() {
	    // Animation complete.
	});
}
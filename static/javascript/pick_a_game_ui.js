$(document).ready(function() {
	alert('hi');
    $('#select').textinput({ preventFocusZoom: true });
    $('#game_select').change( function() {
		var value = $(this).innerHTML();
	    $('#pick_a_game').html(value);
	});
});


function show_modal(){
	$('#pick_a_game_modal').show();
}

function hide_modal(){
	$('#pick_a_game_modal').hide();
}


function submit(){
    $.post('/outreach',{'venue_id':'{{venue_id}}','t_handle':'{{t_handle}}','f_name':'{{f_name}}','t_pic':'{{t_pic}}','game_id':document.getElementsByName('game_id')[0].value,'csrfmiddlewaretoken':document.getElementsByName('csrfmiddlewaretoken')[0].value}, function(data){if (data.error && data.optout == false){$('#status')[0].innerHTML='Uh oh! Looks like there was a problem inviting, please try again in a few minutes';$('#statust').hide();}else if(data.error && data.optout){$('#status')[0].innerHTML='Looks like this person doesn\'t want to receive invitations, please try someone else!';$('#statust').hide();}else{error=false;}});$('#pick_a_game_modal').show();
}


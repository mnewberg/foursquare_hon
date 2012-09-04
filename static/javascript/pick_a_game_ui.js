$(document).ready(function() {
    $('#select').selectmenu({ preventFocusZoom: true });
    $('#game_select').change( function() {
		var value = $(this).val();
	    $('#pick_a_game').html(value);
	});
});

function game_validate(){
var val=document.getElementsByName('game_id')[0].value; if (val==""){return true}else{return false}
}

function show_modal(){
	$('#pick_a_game_modal').show();
}

function hide_modal(){
	$('#pick_a_game_modal').hide();
}





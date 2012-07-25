$(document).ready(function() {

	$('#arrow').on('click', function(){
		twitter_bio();
	});

	$('#back_arrow').on('click', function(){
		game_animation();
	});


});

function twitter_bio(){
	$('#screens').animate({
    	marginLeft: '-320px'
    });
}

function game_animation(){
	$('#screens').animate({
    	marginLeft: '0px'
    });
}
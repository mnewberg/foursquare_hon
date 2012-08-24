$(document).ready(function() {

	$('#arrow').on('click', function(){
		twitter_bio();
	});

	$('#back_arrow').on('click', function(){
		game_animation();
	});

	runIt();
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

function runIt() {
		setTimeout ( $('animation_text').html('P'), 0 );
		setTimeout ( $('animation_text').html('Py'), 100 );
		setTimeout ( $('animation_text').html('Pyr'), 200 );
		setTimeout ( $('animation_text').html('Pyra'), 300 );
		setTimeout ( $('animation_text').html('Pyram'), 400 );
		setTimeout ( $('animation_text').html('Pyrami'), 500 );
		setTimeout ( $('animation_text').html('Pyramid'), 600 );
		setTimeout ( $('animation_text').html('Pyramids'), 700 );

}
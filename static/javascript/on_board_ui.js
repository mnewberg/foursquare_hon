$(document).ready(function() {

	$('#arrow').on('click', function() {
		twitter_bio();
	});	

	$('#back_arrow').on('click', function() {
		game_animation();
	});
	typing();
});

var d=0
var c=0
var i=0



function twitter_bio() {
	$('#screens').animate({
		marginLeft: '-320px'
	});
}

function game_animation() {
	$('#screens').animate({
		marginLeft: '0px'
	});
}

var rappers=["50 Cent","Jay-Z","Biggie"]
function theInterval() {
	$('#animation_text')[0].innerHTML += rappers[i][d];
	d++
	if (d > rappers[i].length && i <= rappers.length-1) {
		$('#animation_text').html('')
		i++;
		d=0;
		} 
		else if (d == rappers[i].length && i == rappers.length-1)
		{
			clearInterval(the_typing);
			runAnimation();
		}

}


function typing() {
	 the_typing=setInterval(theInterval,300)
}

function sample_guesses(){
	$('#sample_guess').html(rappers[c]);
	$('#your_score')[0].innerHTML++;
	c++;
	if (c >= rappers.length){
	    clearInterval(start_guess);scene_3()
	}
}

function scene_2() {
	c=0
	$('#your_score').html('0')
	$('#sample_guess').html('')
	$('#scene_2').fadeIn('slow',function(){start_guess=setInterval(sample_guesses, 1000);})
}

function runAnimation() {
	$('#scene_1').fadeOut('slow',scene_2());

}

var secs = 5;

function timer() {
    secs = secs - 1;
    if (secs >= 0) {
        $('#time_remaining')[0].innerHTML = '0:0' + secs;
    } else {
        clearInterval(the_timer);
        $('#time_remaining').css({
            color: 'red'
        });
        $('#scene_3').fadeOut('fast', function () {
            $('#scene_1').fadeIn('fast');
			$('#animation_text').html('');
			i=0;
			d=0;
			$('#time_remaining').css({color: '#FFFC00'});
	    $('#time_remaining').html('0:05');
			typing();
        });
    }
}

function scene_3() {
	$('#scene_2').fadeOut('slow');
	$('#scene_3').fadeIn('slow');
	secs=5
	the_timer=setInterval(timer, 1000);

}

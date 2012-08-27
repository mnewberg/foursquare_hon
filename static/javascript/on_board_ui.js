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

var text = "Guess an item"
var delay= 1000
i=0
function text_animation(i){
    $('#animation_text').html(word.slice(0,i));
}

function runIt()
{
    var c = 0;
    var interval = setInterval(function() { 
        $('#animation_text')[0].innerHTML += text[c]; 
        c++; 
        if(c >= text.length) clearInterval(interval);
    }, 300);

}

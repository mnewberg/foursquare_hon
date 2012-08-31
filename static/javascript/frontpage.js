$(window).load(function(){
	$('#mask1').delay(3000).fadeOut(3000);step1();});
function step1 (){
	setTimeout(function(){$('#line').animate({width:'400px'},{duration:2000,step:step2()});},6000)
} 
function step2 (){
	$('#line2').animate({width:'400px'},{duration:4000,step:function(){$('#text1').delay(1000).fadeIn('slow');$('#text2').delay(2000).fadeIn('slow');$('#text3').delay(3000).fadeIn('slow');step3();}})
}
function step3 (){
	$('#line3').animate({width:'400px'},{duration:6000})
}
